import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.jobs_page import JobsPage
from pages.job_details_page import JobDetailsPage

@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture
def context(browser):
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture
def page(context):
    page = context.new_page()
    yield page

def test_login_page(page):
    login_page = LoginPage(page)
    login_page.navigate()
    assert "Login" in page.title()

def test_home_page_search(page):
    home_page = HomePage(page)
    assert home_page.search_jobs("Python Developer", "Bangalore", 5)

def test_jobs_page_listing(page):
    jobs_page = JobsPage(page)
    jobs = jobs_page.get_job_listings()
    assert len(jobs) > 0

def test_job_details_page(page):
    job_details_page = JobDetailsPage(page)
    assert hasattr(job_details_page, 'can_apply_directly')
    assert hasattr(job_details_page, 'needs_additional_info')
    assert hasattr(job_details_page, 'submit_application')
