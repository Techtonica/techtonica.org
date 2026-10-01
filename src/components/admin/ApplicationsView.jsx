import React, { useState, useMemo } from 'react';

const ApplicationsView = ({ data }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [activeFilter, setActiveFilter] = useState('All');

  const { applicants, filters, search_placeholder } = data;

  const filteredApplicants = useMemo(() => {
    return applicants.filter(applicant => {
      const matchesSearch = 
        applicant.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
        applicant.email.toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchesFilter = activeFilter === 'All' || applicant.status === activeFilter;
      
      return matchesSearch && matchesFilter;
    });
  }, [searchTerm, activeFilter, applicants]);

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Applications Management</h1>
      
      <div className="flex flex-col md:flex-row gap-4 mb-6 justify-between items-center">
        {/* Search Input */}
        <div className="relative w-full md:w-96">
          <input
            type="text"
            placeholder={search_placeholder}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        {/* Filter Tabs */}
        <div className="flex flex-wrap gap-2">
          {filters.map(filter => (
            <button
              key={filter}
              onClick={() => setActiveFilter(filter)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                activeFilter === filter 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {filter}
            </button>
          ))}
        </div>
      </div>

      {/* Applications Table */}
      <div className="overflow-x-auto bg-white rounded-lg shadow">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-50 border-b">
              <th className="p-4 font-semibold text-gray-600">Name</th>
              <th className="p-4 font-semibold text-gray-600">Email</th>
              <th className="p-4 font-semibold text-gray-600">Score</th>
              <th className="p-4 font-semibold text-gray-600">Status</th>
              <th className="p-4 font-semibold text-gray-600">Submitted</th>
              <th className="p-4 font-semibold text-gray-600">Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredApplicants.length > 0 ? (
              filteredApplicants.map(applicant => (
                <tr key={applicant.id} className="border-b hover:bg-gray-50 transition-colors">
                  <td className="p-4 font-medium">{applicant.name}</td>
                  <td className="p-4 text-gray-600">{applicant.email}</td>
                  <td className="p-4">{applicant.eligibility_score}</td>
                  <td className="p-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-bold ${
                      applicant.status === 'Eligible' ? 'bg-green-100 text-green-700' :
                      applicant.status === 'Ineligible' ? 'bg-red-100 text-red-700' :
                      applicant.status === 'Pending' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-blue-100 text-blue-700'
                    }`}>
                      {applicant.status}
                    </span>
                  </td>
                  <td className="p-4 text-gray-500">{applicant.date_submitted}</td>
                  <td className="p-4">
                    <button className="text-blue-600 hover:underline font-medium">View Details</button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6" className="p-8 text-center text-gray-500">
                  No applications found matching your criteria.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ApplicationsView;
