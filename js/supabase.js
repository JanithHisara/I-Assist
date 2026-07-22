// ---------- SUPABASE & API SUBMISSION HANDLER ----------
const SUPABASE_URL = 'https://mzzragpmkvdvnrletekn.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im16enJhZ3Bta3Zkdm5ybGV0ZWtuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQ2OTAxNjAsImV4cCI6MjEwMDI2NjE2MH0.z8fGn835zUXgy1nsVBuun4DR4aFzsVKhNBiXEqQuFuc';

async function handleFormSubmit(event) {
  event.preventDefault();
  const form = event.target;
  const submitBtn = form.querySelector('button[type="submit"]');
  const submitNote = form.querySelector('.submit-note');

  const name = document.getElementById('briefName').value;
  const email = document.getElementById('briefEmail').value;
  const project_stage = document.getElementById('briefStage').value;
  const details = document.getElementById('briefDetails').value;

  submitBtn.disabled = true;
  const originalBtnText = submitBtn.innerText;
  submitBtn.innerText = 'Sending...';

  const formData = { name, email, project_stage, details };

  try {
    // 1. Try Vercel Serverless Backend API
    const response = await fetch('/api/submit-brief', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });

    if (response.ok) {
      submitNote.style.display = 'block';
      submitNote.style.color = 'var(--signal-bright)';
      submitNote.innerText = "Brief received — saved to database! We'll reply within one business day.";
      form.reset();
      return;
    }

    // 2. Fallback to direct client-side Supabase JS if local preview without Vercel API
    if (window.supabase && SUPABASE_URL && SUPABASE_ANON_KEY) {
      const _supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
      const { data, error } = await _supabase
        .from('project_briefs')
        .insert([formData]);

      if (error) throw error;

      submitNote.style.display = 'block';
      submitNote.style.color = 'var(--signal-bright)';
      submitNote.innerText = "Brief received — saved to database! We'll reply within one business day.";
      form.reset();
      return;
    }

    throw new Error('Submission failed');
  } catch (err) {
    console.error('Submission error:', err);
    submitNote.style.display = 'block';
    submitNote.style.color = '#ef4444';
    submitNote.innerText = 'Failed to submit brief. Please try again.';
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerText = originalBtnText;
  }
}
