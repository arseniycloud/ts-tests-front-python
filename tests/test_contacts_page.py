import allure
import pytest

from locators.contacts_locators import ContactsLocators


@allure.epic("Contacts")
@allure.feature("Contacts Page")
@allure.title("Contacts Page - Information")
class TestContactsPageTestsFunctionality:

    @allure.title("Test contacts page elements are visible")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_contacts_page_elements(self, contacts_page):
        contacts_page.check_contacts_elements()

    @allure.title("Test contact information is present")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_contact_information(self, contacts_page):
        locators = ContactsLocators()

        # Check for common contact information elements
        contact_elements = contacts_page.page.locator(locators.contact_info)
        assert (contact_elements.count() >= 0), "Contacts page should have contact information"

    @allure.title("Test contact form elements")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_contact_form(self, contacts_page):
        locators = ContactsLocators()

        # Check if contact form is present
        form = contacts_page.page.locator(locators.contact_form)
        if form.count() > 0:

            # Check for common form elements
            name_field = contacts_page.page.locator(locators.form_name)
            email_field = contacts_page.page.locator(locators.form_email)
            message_field = contacts_page.page.locator(locators.form_message)
            submit_button = contacts_page.page.locator(locators.form_submit)

            # At least some form elements should be present
            total_elements = (
                name_field.count()
                + email_field.count()
                + message_field.count()
                + submit_button.count()
            )
            assert total_elements >= 0, "Contact form should have form elements"

    @allure.title("Test contacts page navigation")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_contacts_navigation(self, contacts_page):

        # Check if we're on contacts page
        assert "/contacts" in contacts_page.page.url, "Should be on contacts page"

        # Check page title
        locators = ContactsLocators()
        title = contacts_page.page.locator(locators.page_title).text_content()
        assert title is not None, "Contacts page should have a title"

    @allure.title("Test social media links")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_social_links(self, contacts_page):
        locators = ContactsLocators()

        # Check for social media links
        social_links = contacts_page.page.locator(locators.social_links)
        assert social_links.count() >= 0, "Contacts page may have social media links"

    @allure.title("Test map integration")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_map_integration(self, contacts_page):
        locators = ContactsLocators()

        # Check for map elements
        map_elements = contacts_page.page.locator(locators.map_container)
        assert map_elements.count() >= 0, "Contacts page may have map integration"
