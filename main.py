# Read the API Documentation carefully (https://gofile.io/api)
# Create a new account and get token in your profile (https://gofile.io/myprofile)

import os
import requests, datetime, pytz

class FileUploader:
    @staticmethod
    def convertBytes(byteSize):
        units = ["B", "KB", "MB", "GB", "TB", "PB"]

        if byteSize < 1:
            return "0B"

        unitIndex = 0
        while byteSize >= 1024 and unitIndex < len(units) - 1:
            byteSize /= 1024.0
            unitIndex += 1

        return f"{byteSize:.2f} {units[unitIndex]}"
      
    def UploadToGofile(self, path: str, fileName: str = None) -> str | None:

        token = "TOKEN"

        if not os.path.isfile(path):
            print("❌ File không tồn tại:", path)
            return None

        if fileName is None:
            fileName = os.path.basename(path)

        try:
            resServer = requests.get("https://api.gofile.io/servers", headers={
                "User-Agent": "Mozilla/5.0",
                "Authorization": f"Bearer {token}"
            })
            # print("🔄 Server status code:", resServer.status_code) # debug
            # print("🔄 Server content:", resServer.text) #debug

            data = resServer.json()

            server = data["data"]["servers"][0]["name"]
            print("⬆️ Uploading....")
            # Upload
            with open(path, "rb") as f:
                files = {"file": (fileName, f)}
                resUpload = requests.post(
                    f"https://{server}.gofile.io/uploadFile",
                    files=files,
                    headers={
                        "User-Agent": "Mozilla/5.0",
                        "Authorization": f"Bearer {token}"
                    }
                )
                timeUpload = resUpload.json()["data"]["createTime"]
                utcTime = datetime.datetime.utcfromtimestamp(timeUpload)
                vietnamTz = pytz.timezone('Asia/Ho_Chi_Minh')
                vietnamTime = pytz.utc.localize(utcTime).astimezone(vietnamTz)

                size = resUpload.json()["data"]["size"]
                name = resUpload.json()["data"]["name"]

                print(f"📡 Server: {server}")
                print("📤 Status code:", "✅" if resUpload.status_code == 200 else "❌")
                # print("📤 Upload response:", resUpload.text)
                print("🕒 Time:", vietnamTime.strftime('%Y-%m-%d %H:%M:%S') + " (GMT+7)")
                print("💾 Size:", self.convertBytes(size))
                print("📂 Name:", name)

                uploadData = resUpload.json()

            if uploadData["status"] == "ok":
                return uploadData["data"]["downloadPage"]
            else:
                print("❌ Upload lỗi:", uploadData)
                return None

        except Exception as e:
            print("❌ Lỗi:", e)
            return None

if __name__ == "__main__":
    uploader = FileUploader()
    url = uploader.UploadToGofile("YOUR_FILE_PATH") # Example: text.txt
    if url is not None:
        print("📦 URL:", url)
