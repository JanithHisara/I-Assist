// ---------- SUPABASE BACKEND SERVICE INTEGRATION ----------
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

  if (!SUPABASE_URL || !SUPABASE_ANON_KEY || SUPABASE_URL === 'YOUR_SUPABASE_URL') {
    setTimeout(() => {
      submitNote.style.display = 'block';
      submitNote.style.color = 'var(--signal-bright)';
      submitNote.innerText = "Brief received — (Note: Please configure SUPABASE_URL & KEY to save in DB).";
      submitBtn.disabled = false;
      submitBtn.innerText = originalBtnText;
      form.reset();
    }, 500);
    return;
  }

  try {
    const _supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
    const { data, error } = await _supabase
      .from('project_briefs')
      .insert([{ name, email, project_stage, details }]);

    if (error) throw error;

    submitNote.style.display = 'block';
    submitNote.style.color = 'var(--signal-bright)';
    submitNote.innerText = "Brief received — saved to database! We'll reply within one business day.";
    form.reset();
  } catch (err) {
    console.error('Supabase submission error:', err);
    submitNote.style.display = 'block';
    submitNote.style.color = '#ef4444';
    submitNote.innerText = 'Failed to submit brief. Please check credentials or try again.';
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerText = originalBtnText;
  }
}
