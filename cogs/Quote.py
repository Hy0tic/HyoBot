from discord.ext import commands
import re
import requests
import os
import boto3
from botocore.client import Config
import uuid

endpoint_url = 'https://1937634c51f95aa498801e9e19f2c242.r2.cloudflarestorage.com'
access_url = 'https://bucket.bn-chat.net'
access_key = os.environ.get("cloudflare_access_key")
secret_key = os.environ.get("cloudflare_secret_key")
bucket_name = 'pfp'

# Create a session and client
session = boto3.session.Session()
client = session.client('s3',
                        endpoint_url=endpoint_url,
                        aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key,
                        config=Config(signature_version='s3v4'))

class Quote(commands.Cog):
    def __init__(self, BOT):
        self.BOT = BOT

    @commands.Cog.listener()
    async def on_ready(self):
        print('Quote cog ready') 
    
    @commands.command(help="upload")
    async def upload(self, ctx):
        author_id = ctx.author.id
        if(author_id != 422848768166199302 and author_id != 451176601644957698):
            await ctx.send("not authorized to use this command")
            return
        print('Uploading image to R2 bucket')
        # Upload the file
        try:
            print('downloading image')
            if not ctx.message.attachments and not ctx.message.content:
                await ctx.send("No image found in the message.")
                return

            imageId = str(uuid.uuid4())
            save_file_name = imageId + ".png"
            object_name = imageId
            save_directory = "downloaded_images"  # Specify your folder
            file_path = os.path.join(save_directory, save_file_name)
            os.makedirs(save_directory, exist_ok=True)  # Create folder if it doesn't exist

            # Handle image URLs in the message content
            for word in ctx.message.content.split():
                if word.startswith("http"):
                    try:
                        file_name = download_image(word, save_directory, save_file_name)
                    except Exception as e:
                        await ctx.send(f"Failed to download image from URL: {word}\nError: {e}")
                        return

            # Handle image attachments
            for attachment in ctx.message.attachments:
                if any(attachment.filename.lower().endswith(ext) for ext in [".jpg", ".png", ".jpeg", ".gif", ".webp"]):
                    file_name = attachment.filename
                    file_path = os.path.join(save_directory, file_name)
                    await attachment.save(file_path)
                    await ctx.send(f"Image attachment downloaded as {file_name}")

            client.upload_file(file_path, bucket_name, object_name)
            print(f'File {file_path} uploaded to {bucket_name}/{object_name}')
            file_url = f'{access_url}/{object_name}'
            await ctx.send(f'File uploaded to: {file_url}')

            # Check if the file exists
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f'File {file_path} has been deleted successfully.')
            else:
                print(f'File {file_path} does not exist.')
        except Exception as e:
            print(f'Error uploading file: {e}')

 
async def setup(BOT):
    await BOT.add_cog(Quote(BOT))  

def download_image(url, save_directory, file_name):
    response = requests.get(url)
    response.raise_for_status()  # Check for any errors during the request

    save_path = os.path.join(save_directory, file_name)

    with open(save_path, "wb") as file:
        file.write(response.content)

