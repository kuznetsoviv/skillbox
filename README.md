# Terraform Configuration

## Environment Variables Setup

Run these commands in your console to configure Terraform with Yandex Cloud:

```bash
export YC_TOKEN=$(yc config get token)
export YC_CLOUD_ID=$(yc config get cloud-id)
export YC_FOLDER_ID=$(yc config get folder-id)
