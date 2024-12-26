import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from datetime import datetime
from email import encoders


class EmailManager:
    def __init__(self):
        self.sender_email = os.getenv("EMAIL_ADDRESS")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT"))
        self.receiver_email = 'Daniel.Sibaja1@ibm.com'
        self.subject = None
        self.email_template_path = 'C:\DEV\Py_Selenium_Script 1\email\email.template.html'
        self.subject_prefix="IUC Document"

    def load_email_template(self):
        try:
            # Load the HTML content from an external file
            with open(self.email_template_path, "r") as file:
                html_content = file.read()
            return html_content
        except FileNotFoundError:
            print(f"Error: The file {self.email_template_path} was not found.")
            return None
        except IOError:
            print(f"Error: There was an issue reading the file {self.email_template_path}.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def generate_unique_subject(self):
        try:
            # Get the current timestamp with seconds
            timestamp = datetime.now().strftime("%B %d, %Y, %I:%M:%S %p") 
            # Combine the prefix and readable timestamp
            unique_subject = f"{self.subject_prefix}: {timestamp}"
            return unique_subject
        except Exception as e:
            # Catch any exception
            print(f"Error occurred while generating the unique subject: {e}")
            return None  
        
    def send_email(self, file_attachment_path):
        try:
            # Creating unique subject line
            self.subject = self.generate_unique_subject()

            #Loading HTML content from email template
            self.email_template_path = self.load_email_template()

            # Create the MIME multipart message
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = self.receiver_email
            msg["Subject"] = self.subject

            # Attach the HTML body
            try:
                msg.attach(MIMEText(self.email_template_path, "html"))
            except Exception as e:
                print(f"Error attaching HTML content: {e}")
                return 

            # Attach the document (PDF/Word etc.)
            try:
                with open(file_attachment_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition", f"attachment; filename={os.path.basename(file_attachment_path)}"
                    )
                    # Attach the document to the email
                    msg.attach(part)
            except FileNotFoundError as e:
                print(f"Attachment file not found: {e}")
                return  # Return early if the attachment can't be found
            except Exception as e:
                print(f"Error attaching file: {e}")
                return  # Return early if any other error occurs during attachment

            # Send the email through the SMTP server
            try:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()  # Secure the connection
                server.login(self.sender_email, self.password)
                text = msg.as_string()
                server.sendmail(self.sender_email, self.receiver_email, text)
                print("Email sent successfully.")
            except smtplib.SMTPException as e:
                print(f"SMTP error occurred: {e}")
            except Exception as e:
                print(f"Error sending email: {e}")
            finally:
                server.quit()

        except Exception as e:
            print(f"Unexpected error: {e}")