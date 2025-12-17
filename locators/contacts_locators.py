from dataclasses import dataclass


@dataclass
class ContactsLocators:
    """Contacts page locators"""
    # Page structure
    page_title = "h1, h2, .title"
    page_container = ".contacts-page, .contact-page"

    # Contact information
    contact_info = ".contact-info, .contacts, .contact-details"
    contact_section = ".contact-section, .info-section"

    # Contact details
    email_link = "a[href^='mailto:']"
    phone_link = "a[href^='tel:']"
    phone_text = "text=/\\+?[0-9\\s\\-\\(\\)]{10,}/"
    address = ".address, .location, .office-address"

    # Contact form
    contact_form = ".contact-form, form"
    form_name = "input[name*='name'], input[placeholder*='имя']"
    form_email = "input[type='email'], input[name*='email']"
    form_phone = "input[type='tel'], input[name*='phone']"
    form_subject = "input[name*='subject'], input[placeholder*='тема']"
    form_message = "textarea, input[name*='message']"
    form_submit = "button[type='submit'], input[type='submit']"

    # Form validation
    form_error = ".form-error, .field-error, .validation-error"
    form_success = ".form-success, .success-message"

    # Social media links
    social_links = ".social-links, .social-media"
    youtube_link = "a[href*='youtube']"
    vk_link = "a[href*='vk.com']"
    facebook_link = "a[href*='facebook']"
    instagram_link = "a[href*='instagram']"
    linkedin_link = "a[href*='linkedin']"
    telegram_link = "a[href*='telegram']"

    # Map integration
    map_container = "iframe[src*='map'], .map, [class*='map']"
    map_frame = "iframe[src*='google'], iframe[src*='yandex']"

    # Office information
    office_hours = ".office-hours, .working-hours"
    office_location = ".office-location, .location-info"

    # Team section
    team_section = ".team-section, .staff-section"
    team_member = ".team-member, .staff-member"
    member_name = ".member-name, .staff-name"
    member_position = ".member-position, .staff-position"
    member_photo = ".member-photo, .staff-photo"

    # FAQ section
    contacts_faq = ".contacts-faq, .faq-section"
    faq_question = ".faq-question, .question"
    faq_answer = ".faq-answer, .answer"

    # Additional information
    company_info = ".company-info, .about-company"
    legal_info = ".legal-info, .legal-documents"
    privacy_policy = "a[href*='privacy'], a[href*='конфиденциальность']"
    terms_of_service = "a[href*='terms'], a[href*='условия']"

    # Contact methods
    contact_methods = ".contact-methods, .ways-to-contact"
    phone_method = ".phone-method, .call-us"
    email_method = ".email-method, .write-us"
    chat_method = ".chat-method, .live-chat"

    # Business hours
    business_hours = ".business-hours, .opening-hours"
    hours_weekday = ".hours-weekday, .weekday-hours"
    hours_weekend = ".hours-weekend, .weekend-hours"

    # Emergency contact
    emergency_contact = ".emergency-contact, .urgent-contact"
    emergency_phone = ".emergency-phone, .urgent-phone"

    # Newsletter signup
    newsletter_signup = ".newsletter-signup, .subscribe"
    newsletter_email = ".newsletter-email, input[placeholder*='newsletter']"
    newsletter_button = ".newsletter-button, .subscribe-button"

    # Feedback section
    feedback_section = ".feedback-section, .reviews-section"
    feedback_form = ".feedback-form, .review-form"
    rating_stars = ".rating-stars, .star-rating"

    # Support information
    support_info = ".support-info, .help-info"
    support_hours = ".support-hours, .help-hours"
    support_email = ".support-email, .help-email"
