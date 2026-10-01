import { google } from 'googleapis';
import fs from 'fs';
import path from 'path';

const AUTH = {
  client_email: process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL,
  private_key: process.env.GOOGLE_PRIVATE_KEY?.replace(/\\n/g, '\n'),
};

const SCOPES = ['https://www.googleapis.com/auth/drive.file'];

export const googleDriveService = {
  async uploadFile(fileBuffer: Buffer, fileName: string, mimeType: string, folderId: string) {
    const auth = new google.auth.JWT(
      AUTH.client_email,
      null,
      AUTH.private_key,
      SCOPES
    );

    const drive = google.drive({ version: 'v3', auth });

    const fileMetadata = {
      name: fileName,
      parents: [folderId],
    };

    const media = {
      mimeType,
      body: require('stream').Readable.from(fileBuffer),
    };

    try {
      const response = await drive.files.create({
        requestBody: fileMetadata,
        media: media,
        fields: 'id, webViewLink',
      });

      return response.data;
    } catch (error) {
      console.error('Error uploading to Google Drive:', error);
      throw new Error('Failed to upload document to secure storage');
    }
  },

  async setFilePermissions(fileId: string, email: string) {
    const auth = new google.auth.JWT(
      AUTH.client_email,
      null,
      AUTH.private_key,
      SCOPES
    );
    const drive = google.drive({ version: 'v3', auth });

    await drive.permissions.create({
      fileId,
      requestBody: {
        role: 'reader',
        type: 'user',
        emailAddress: email,
      },
    });
  }
};
