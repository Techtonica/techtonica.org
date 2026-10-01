import React, { useState } from 'react';
import { CheckCircle, XCircle, AlertTriangle, Edit2, MessageSquare, PlusCircle } from 'lucide-react';

interface ApplicationDetails {
  wpm_score: number;
  wpm_accuracy: string;
  two_references: boolean;
  freecodecamp_complete: boolean;
  gender: string;
  computer_literate: string;
  recent_bootcamp: string;
  stable_housing: string;
}

interface Applicant {
  id: number;
  name: string;
  email: string;
  eligibility_score: number;
  status: string;
  date_submitted: string;
  details: ApplicationDetails;
  admin_notes: string[];
}

const ApplicationDetailView = ({ applicant, onUpdate }: { applicant: Applicant, onUpdate: (id: number, updates: any) => void }) => {
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [isNoteOpen, setIsNoteOpen] = useState(false);
  const [isMsgOpen, setIsMsgOpen] = useState(false);
  const [noteText, setNoteText] = useState('');
  const [msgText, setMsgText] = useState('');

  const checkEligibility = (value: any, criteria: (v: any) => boolean, isWarning = false) => {
    if (isWarning) return <AlertTriangle className="text-yellow-500" size={20} title="Manual Review Required" />;
    return criteria(value) ? <CheckCircle className="text-green-500" size={20} /> : <XCircle className="text-red-500" size={20} />;
  };

  const handleAddNote = () => {
    const timestamp = new Date().toLocaleString();
    onUpdate(applicant.id, { 
      admin_notes: [...applicant.admin_notes, `[${timestamp}] ${noteText}`] 
    });
    setNoteText('');
    setIsNoteOpen(false);
  };

  const handleSendMessage = () => {
    const timestamp = new Date().toLocaleString();
    onUpdate(applicant.id, { 
      admin_notes: [...applicant.admin_notes, `[${timestamp}] Message sent to applicant: ${msgText}`] 
    });
    setMsgText('');
    setIsMsgOpen(false);
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">{applicant.name} - Application Detail</h2>
        <div className="flex gap-2">
          <button onClick={() => setIsEditOpen(true)} className="flex items-center gap-1 px-3 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
            <Edit2 size={16} /> Edit
          </button>
          <button onClick={() => setIsMsgOpen(true)} className="flex items-center gap-1 px-3 py-2 bg-gray-600 text-white rounded hover:bg-gray-700">
            <MessageSquare size={16} /> Message
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="space-y-4">
          <div className="flex justify-between p-2 border-b">
            <span>Eligibility Score:</span>
            <span className="font-bold">{applicant.eligibility_score}</span>
          </div>
          <div className="flex justify-between p-2 border-b">
            <span>WPM Score (50+):</span>
            <div className="flex items-center gap-2">
              <span>{applicant.details.wpm_score}</span>
              {checkEligibility(applicant.details.wpm_score, (v) => v >= 50)}
            </div>
          </div>
          <div className="flex justify-between p-2 border-b">
            <span>WPM Accuracy (80%+):</span>
            <div className="flex items-center gap-2">
              <span>{applicant.details.wpm_accuracy}</span>
              {checkEligibility(applicant.details.wpm_accuracy, (v) => parseInt(v) >= 80)}
            </div>
          </div>
          <div className="flex justify-between p-2 border-b">
            <span>Two References:</span>
            <div className="flex items-center gap-2">
              <span>{applicant.details.two_references ? 'Yes' : 'No'}</span>
              {checkEligibility(applicant.details.two_references, (v) => v === true)}
            </div>
          </div>
          <div className="flex justify-between p-2 border-b">
            <span>FreeCodeCamp Complete:</span>
            <div className="flex items-center gap-2">
              <span>{applicant.details.freecodecamp_complete ? 'Yes' : 'No'}</span>
              {checkEligibility(null, null, true)}
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <div className="flex justify-between p-2 border-b">
            <span>Gender (Not cis-male):</span>
            <div className="flex items-center gap-2">
              <span>{applicant.details.gender}</span>
              {checkEligibility(applicant.details.gender, (v) => v.toLowerCase() !== 'man' && v.toLowerCase() !== 'cis-male')}
            </div>
          </div>
          <div className="flex justify-between p-2 border-b">
            <span>Computer Literate:</span>
            <div className="flex items-center gap-2">
              <span>{applicant.details.computer_literate}</span>
              {checkEligibility(applicant.details.computer_literate, (v) => v === 'Yes')}
            </div>
          </div>
          <div className="flex justify-between p-2 border-b">
            <span>Recent Bootcamp:</span>
            <div className="flex items-center gap-2">
              <span>{applicant.details.recent_bootcamp}</span>
              {checkEligibility(applicant.details.recent_bootcamp, (v) => v === 'No')}
            </div>
          </div>
          <div className="flex justify-between p-2 border-b">
            <span>Stable Housing:</span>
            <div className="flex items-center gap-2">
              <span>{applicant.details.stable_housing}</span>
              {checkEligibility(applicant.details.stable_housing, (v) => v === 'Yes')}
            </div>
          </div>
        </div>
      </div>

      <div className="mt-6">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-semibold">Admin Notes</h3>
          <button onClick={() => setIsNoteOpen(true)} className="text-blue-600 flex items-center gap-1 text-sm">
            <PlusCircle size={14} /> Add Note
          </button>
        </div>
        <div className="bg-gray-50 p-4 rounded border max-h-40 overflow-y-auto">
          {applicant.admin_notes.map((note, idx) => (
            <p key={idx} className="text-sm text-gray-600 mb-2 border-b pb-1">{note}</p>
          ))}
        </div>
      </div>

      {/* Modals */}
      {(isEditOpen || isNoteOpen || isMsgOpen) && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg w-full max-w-md">
            {isEditOpen && (
              <>
                <h3 className="text-xl font-bold mb-4">Edit Application</h3>
                <div className="space-y-4">
                  <label className="block">
                    <span className="text-sm">Status</span>
                    <input type="text" className="w-full border p-2 rounded" defaultValue={applicant.status} />
                  </label>
                  <label className="block">
                    <span className="text-sm">Eligibility Score</span>
                    <input type="number" className="w-full border p-2 rounded" defaultValue={applicant.eligibility_score} />
                  </label>
                </div>
                <div className="flex justify-end gap-2 mt-6">
                  <button onClick={() => setIsEditOpen(false)} className="px-4 py-2 text-gray-600">Cancel</button>
                  <button onClick={() => {
                    const timestamp = new Date().toLocaleString();
                    onUpdate(applicant.id, { admin_notes: [...applicant.admin_notes, `[${timestamp}] Application fields edited by admin`] });
                    setIsEditOpen(false);
                  }} className="px-4 py-2 bg-blue-600 text-white rounded">Save</button>
                </div>
              </>
            )}

            {isNoteOpen && (
              <>
                <h3 className="text-xl font-bold mb-4">Add Admin Note</h3>
                <textarea 
                  className="w-full border p-2 rounded h-32" 
                  value={noteText} 
                  onChange={(e) => setNoteText(e.target.value)}
                  placeholder="Enter internal note..."
                />
                <div className="flex justify-end gap-2 mt-6">
                  <button onClick={() => setIsNoteOpen(false)} className="px-4 py-2 text-gray-600">Cancel</button>
                  <button onClick={handleAddNote} className="px-4 py-2 bg-blue-600 text-white rounded">Save Note</button>
                </div>
              </>
            )}

            {isMsgOpen && (
              <>
                <h3 className="text-xl font-bold mb-4">Message Applicant</h3>
                <textarea 
                  className="w-full border p-2 rounded h-32" 
                  value={msgText} 
                  onChange={(e) => setMsgText(e.target.value)}
                  placeholder="Type your message to the applicant..."
                />
                <div className="flex justify-end gap-2 mt-6">
                  <button onClick={() => setIsMsgOpen(false)} className="px-4 py-2 text-gray-600">Cancel</button>
                  <button onClick={handleSendMessage} className="px-4 py-2 bg-blue-600 text-white rounded">Send Message</button>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ApplicationDetailView;
