import { Request, Response } from 'express';
import { googleDriveService } from '../services/googleDriveService';

export const handleFileUpload = async (req: Request, res: Response) => {
  try {
    const { file } = req;
    if (!file) {
      return res.status(400).json({ message: 'No file uploaded' });
    }

    const folderId = process.env.GOOGLE_DRIVE_FOLDER_ID;
    if (!folderId) {
      throw new Error('Google Drive Folder ID not configured');
    }

    const uploadResult = await googleDriveService.uploadFile(
      file.buffer,
      `${req.body.applicantName}_${file.originalname}`,
      file.mimetype,
      folderId
    );

    return res.status(200).json({
      message: 'Document uploaded successfully!',
      fileId: uploadResult.id,
    });
  } catch (error: any) {
    return res.status(500).json({ message: error.message });
  }
};
