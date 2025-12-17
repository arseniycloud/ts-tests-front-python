#!/usr/bin/env python3
"""
Generate enhanced Telegram notifications for test runs.
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional


def get_env(key: str, default: str = "") -> str:
    """Get environment variable with default."""
    return os.getenv(key, default)


def load_ctrf_report(report_path: str = "reports/ctrf-report.json") -> Optional[Dict]:
    """Load CTRF report JSON."""
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading CTRF report: {e}", file=sys.stderr)
        return None


def generate_progress_bar(rate: float, length: int = 10) -> str:
    """Generate a progress bar using block characters for mobile display."""
    filled = round(rate * length)
    return "▰" * filled + "▱" * (length - filled)


def format_duration(seconds: int) -> str:
    """Format duration in human-readable format."""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}m {secs}s"


def get_trend_emoji(_current_passed: int, _current_total: int, _prev_run_number: int) -> str:
    """
    Get trend emoji by comparing with previous run.
    In real implementation, you would fetch previous run data from GitHub API or storage.
    """
    # Placeholder for trend calculation
    # You can implement actual comparison logic here
    return "→"  # Stable, could be ↑ (improvement) or ↓ (regression)


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def extract_failed_tests(ctrf_data: Dict) -> List[Dict]:
    """Extract failed test details from CTRF report."""
    failed_tests = []

    try:
        tests = ctrf_data.get('results', {}).get('tests', [])
        for test in tests:
            if test.get('status') == 'failed':
                # Extract error message
                message = test.get('message', 'No error message')

                # Extract file path from test name or extra data
                file_path = test.get('filePath', 'unknown')
                line_number = test.get('line', 0)

                # Duration in ms to seconds
                duration_ms = test.get('duration', 0)
                duration_sec = duration_ms / 1000 if duration_ms else 0

                # Retries
                retries = test.get('retries', 0)
                flaky = test.get('flaky', False)

                failed_tests.append({
                    'name': test.get('name', 'Unknown Test'),
                    'message': message,
                    'file': file_path,
                    'line': line_number,
                    'duration': duration_sec,
                    'retries': retries,
                    'flaky': flaky
                })
    except Exception as e:
        print(f"Error extracting failed tests: {e}", file=sys.stderr)

    return failed_tests


def determine_status(total: int, pass_rate: float) -> tuple[str, str]:
    """Determine status and emoji based on test results."""
    if total == 0:
        return "⚠️ NO TESTS", "⚠️"
    if pass_rate == 100:
        return "✅ PASSED", "✅"
    if pass_rate >= 95:
        return f"🟢 PARTIALLY PASSED ({pass_rate:.1f}%)", "🟢"
    if pass_rate >= 85:
        return f"🟠 PARTIALLY PASSED ({pass_rate:.1f}%)", "🟠"
    return f"❌ FAILED ({pass_rate:.1f}%)", "❌"


def get_title_for_event(event_name: str) -> str:
    """Get title based on GitHub event type."""
    title_map = {
        'push': "🚀 Push Test Run",
        'pull_request': "🔀 Pull Request Test Run",
        'workflow_dispatch': "👾 Manual Test Run",
        'repository_dispatch': "🚀 Remote RM: Regression",
        'schedule': "🌃 Nightly Test Run",
    }
    return title_map.get(event_name, "🧪 Test Run")


def calculate_timing_info(start_ts: int, total: int) -> tuple[str, str, str]:
    """Calculate timing information from start timestamp."""
    if start_ts <= 0:
        return "N/A", "N/A", "N/A"

    stop_ts = int(datetime.now().timestamp())
    duration_sec = stop_ts - start_ts
    duration_str = format_duration(duration_sec)

    msk_tz = timezone(timedelta(hours=3))
    start_dt = datetime.fromtimestamp(start_ts, tz=msk_tz)
    start_time_str = start_dt.strftime('%Y-%m-%d %H:%M:%S MSK')

    avg_per_test = (duration_sec / total) if total > 0 else 0
    avg_str = f"{avg_per_test:.1f}s"

    return start_time_str, duration_str, avg_str


def format_failed_tests_section(failed_tests: List[Dict], max_show: int = 3) -> List[str]:
    """Format failed tests section for message."""
    lines = []
    if not failed_tests:
        return lines

    lines.append(f"<b>Failed Test{'s' if len(failed_tests) > 1 else ''}:</b>")
    lines.append("")

    for test in failed_tests[:max_show]:
        test_name = escape_html(test['name'])
        lines.append(f"📂 {test_name}")

    if len(failed_tests) > max_show:
        lines.append(f"<i>... and {len(failed_tests) - max_show} more failed tests</i>")

    lines.append("")
    return lines


def format_commit_author(commit_author: str) -> str:
    """Format commit author display name."""
    if 'bot]' in commit_author.lower() or commit_author.lower() == 'github-actions':
        return "🤖 GitHub Actions"
    return f"@{commit_author}"


def generate_telegram_message() -> str:
    """Generate enhanced Telegram message."""
    ctrf_data = load_ctrf_report()
    if not ctrf_data:
        return "<b>⚠️ Test Run</b>\n\nNo test results available"

    summary = ctrf_data.get('results', {}).get('summary', {})
    total = summary.get('tests', 0)
    passed = summary.get('passed', 0)
    failed = summary.get('failed', 0)
    skipped = summary.get('skipped', 0)

    pass_rate = (passed / total * 100) if total > 0 else 0
    pass_rate_normalized = pass_rate / 100
    progress_bar = generate_progress_bar(pass_rate_normalized)
    status, _ = determine_status(total, pass_rate)

    event_name = get_env('GITHUB_EVENT_NAME', 'unknown')
    run_number = get_env('GITHUB_RUN_NUMBER', '0')
    branch = get_env('GITHUB_REF_NAME', 'unknown')
    test_type = get_env('TEST_TYPE', 'unknown')
    browser = get_env('BROWSER', 'chromium')
    device = get_env('DEVICE', 'desktop')

    # Проверяем, есть ли данные о внешнем репозитории (remote trigger)
    source_repo = get_env('SOURCE_REPO', '')
    source_commit = get_env('SOURCE_COMMIT', '')
    source_branch = get_env('SOURCE_BRANCH', '')
    pr_number = get_env('PR_NUMBER', '')
    pr_url = get_env('PR_URL', '')

    # Используем данные из внешнего репозитория, если они есть
    if source_repo and source_commit and source_repo != 'unknown':
        commit_sha_full = source_commit
        branch = source_branch or branch
    else:
        commit_sha_full = get_env('GITHUB_SHA', 'unknown')

    commit_sha = commit_sha_full[:7] if commit_sha_full != 'unknown' else 'unknown'
    commit_message = get_env('COMMIT_MESSAGE', 'No message')
    commit_author = get_env('COMMIT_AUTHOR', '')
    github_actor = commit_author or get_env('GITHUB_ACTOR', 'unknown')

    start_ts_file = Path('reports/test-start-ts.txt')
    start_ts = int(start_ts_file.read_text().strip() or 0) if start_ts_file.exists() else 0
    start_time_str, duration_str, avg_str = calculate_timing_info(start_ts, total)

    repo_url = get_env('GITHUB_SERVER_URL', 'https://github.com')
    repo_name = get_env('GITHUB_REPOSITORY', 'unknown/repo')
    run_id = get_env('GITHUB_RUN_ID', '0')
    run_url = f"{repo_url}/{repo_name}/actions/runs/{run_id}"
    artifacts_url = f"{run_url}#artifacts"
    repo_link = f"{repo_url}/{repo_name}"
    actions_url = f"{repo_url}/{repo_name}/actions"

    # Формируем ссылку на коммит (из внешнего репозитория, если есть)
    if source_repo and source_commit and source_repo != 'unknown':
        commit_url = f"{repo_url}/{source_repo}/commit/{commit_sha_full}"
    else:
        commit_url = f"{repo_url}/{repo_name}/commit/{commit_sha_full}"

    title = get_title_for_event(event_name)

    lines = [
        f"<b>{title} <a href=\"{actions_url}\">#{run_number}</a></b>",
        "",
        f"<b>Status:</b> {status}",
        f"<b>Branch:</b> <code>{branch}</code>",
        f"<b>Pass Rate:</b> {pass_rate:.1f}% [{progress_bar}]",
        "",
    ]

    prev_run = int(run_number) - 1
    if failed > 0 and prev_run > 0:
        trend_text = f"📈 <b>Trend:</b> ↓ {failed} regression{'s' if failed > 1 else ''} (vs #{prev_run})"
        lines.append(trend_text)
        lines.append("")

    lines.extend([
        "<b>⏰ Timing:</b>",
        f"- Started: {start_time_str}",
        f"- Duration: {duration_str}",
        f"- Avg per test: {avg_str}",
        "",
        "<b>💬 Parameters:</b>",
        f"- {test_type} | {browser} | {device}",
        "",
        "<b>📊 Results:</b>",
        f"- Total: {total}",
        f"- Passed: ✅ {passed}",
        f"- Failed: ‼️ {failed}",
        f"- Skipped: ⏭ {skipped}",
        "",
    ])

    if failed > 0:
        failed_tests = extract_failed_tests(ctrf_data)
        lines.extend(format_failed_tests_section(failed_tests))

    # Add PR info if available (for remote triggers)
    if pr_number and pr_url:
        pr_line = f"<b>🔀 PR:</b> <a href=\"{pr_url}\">#{pr_number}</a>"
        lines.append(pr_line)
        lines.append("")

    # Add commit info only if commit SHA is valid
    if commit_sha_full and commit_sha_full != 'unknown':
        commit_msg_short = escape_html(truncate_text(commit_message, 40))
        author_display = format_commit_author(github_actor)
        commit_line = f"<b>📝 Commit:</b> <a href=\"{commit_url}\">{commit_sha}</a>"

        lines.extend([
            commit_line,
            f"<b>Author:</b> {author_display}",
            f"<b>Message:</b> \"{commit_msg_short}\"",
            "",
        ])

    lines.extend([
        "<b>🔗 Links:</b>",
        f"<a href=\"{run_url}\">View Run</a> • <a href=\"{artifacts_url}\">Artifacts</a> • <a href=\"{repo_link}\">Repo</a>",
    ])

    return "\n".join(lines)


def main():
    """Main function."""
    message = generate_telegram_message()

    # Output to file for GitHub Actions
    output_file = Path('telegram-report.html')
    output_file.write_text(message, encoding='utf-8')

    # Also print to stdout
    print(message)

    # Set GitHub Actions output
    github_output = get_env('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a', encoding='utf-8') as f:
            f.write("message<<TELEGRAM_EOF\n")
            f.write(message)
            f.write("\nTELEGRAM_EOF\n")


if __name__ == '__main__':
    main()
