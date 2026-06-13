async function uploadFilesOnly(endpoint, fileMappings, extraFields = {}) {
  const formData = new FormData();

  fileMappings.forEach(({ inputId, fieldName }) => {
    const input = document.getElementById(inputId);
    if (!input || !input.files) return;

    for (const file of input.files) {
      formData.append(fieldName, file);
    }
  });

  Object.entries(extraFields).forEach(([key, value]) => {
    if (value !== null && value !== undefined && value !== "") {
      formData.append(key, value);
    }
  });

  const response = await fetch(endpoint, {
    method: "POST",
    body: formData,
  });

  const result = await response.json();

  if (!response.ok || !result.success) {
    throw new Error(result.error || "File upload failed.");
  }

  return result;
}
