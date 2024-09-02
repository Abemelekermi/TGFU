import argparse
from dotenv import load_dotenv
import requests
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm

def get_mime_type(file_path):
    # Determine the MIME type based on the file extension
    file_extension = os.path.splitext(file_path)[1].lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.mp4': 'video/mp4',
        '.avi': 'video/avi',
        '.mov': 'video/quicktime',
        '.mkv': 'video/x-matroska',
        '.pdf': 'application/pdf',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.xls': 'application/vnd.ms-excel',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.ppt': 'application/vnd.ms-powerpoint',
        '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        '.txt': 'text/plain',
        '.zip': 'application/zip',
        '.rar': 'application/x-rar-compressed',
        '.7z': 'application/x-7z-compressed',
        '.mp3': 'audio/mpeg',
        '.wav': 'audio/wav',
        '.ogg': 'audio/ogg',
        '.flac': 'audio/flac',
        # Add more MIME types as needed
    }
    return mime_types.get(file_extension, 'application/octet-stream')

def upload_file(file_path, chat_id, token):
    mime_type = get_mime_type(file_path)
    file_size = os.path.getsize(file_path)

    with open(file_path, 'rb') as file:
        # Create a MultipartEncoder to handle the file upload
        encoder = MultipartEncoder(fields={'document': ('filename', file, mime_type)})

        # Create a progress bar
        progress_bar = tqdm(total=file_size, unit='B', unit_scale=True, desc='Uploading')

        # Create a MultipartEncoderMonitor to track the upload progress
        def upload_callback(monitor):
            progress_bar.update(monitor.bytes_read - progress_bar.n)

        monitor = MultipartEncoderMonitor(encoder, upload_callback)

        # Prepare the URL for sending the file
        url = f"https://api.telegram.org/bot{token}/sendDocument"

        # Send the file with progress tracking
        response = requests.post(url, data=monitor, headers={'Content-Type': monitor.content_type}, params={'chat_id': chat_id})
        response.raise_for_status()  

    return response.json()

def get_chat_id(token):
    MessageIdUrl = f"https://api.telegram.org/bot{token}/getUpdates"
    response = requests.get(MessageIdUrl).json()
    if not response["result"]:
        raise ValueError("No updates found")
    return response["result"][0]["message"]["from"]["id"]

def main():
    parser = argparse.ArgumentParser(description="Upload a file to Telegram")
    parser.add_argument("--file_path", help="Path to the file to be uploaded")
    parser.add_argument("--chat_id",required=True, help="your chat id")

    args = parser.parse_args()

    try:
        load_dotenv()
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        file_path = args.file_path
        chat_id = args.chat_id if args.chat_id else get_chat_id(token)
        # Upload the file
        result = upload_file(file_path, chat_id, token)
        print(result)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except requests.exceptions.RequestException as e:
        print(f"Error: An error occurred while making the request: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()