from pyhunter import PyHunter

# Initialize PyHunter with your API key
hunter = PyHunter('your_api_key_here')

def extract_emails_from_website(url):
    try:
        result = hunter.domain_search(domain=url)
        emails = [email['value'] for email in result['emails']]
        return emails
    except Exception as e:
        print(f"Error extracting emails: {e}")
        return []

def extract_emails_from_linkedin(linkedin_url):
    try:
        result = hunter.linkedin_email(email=linkedin_url)
        return result['email']
    except Exception as e:
        print(f"Error extracting email from LinkedIn: {e}")
        return None

# Example usage
website_url = 'example.com'
linkedin_url = 'https://www.linkedin.com/in/example_profile'

website_emails = extract_emails_from_website(website_url)
print("Emails from website:", website_emails)

linkedin_email = extract_emails_from_linkedin(linkedin_url)
print("Email from LinkedIn:", linkedin_email)
