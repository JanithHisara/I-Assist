import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = process.env.SUPABASE_URL || 'https://mzzragpmkvdvnrletekn.supabase.co';
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im16enJhZ3Bta3Zkdm5ybGV0ZWtuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQ2OTAxNjAsImV4cCI6MjEwMDI2NjE2MH0.z8fGn835zUXgy1nsVBuun4DR4aFzsVKhNBiXEqQuFuc';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { name, email, project_stage, details } = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {});

  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email are required fields' });
  }

  try {
    const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
    const { data, error } = await supabase
      .from('project_briefs')
      .insert([{ name, email, project_stage, details }]);

    if (error) throw error;

    return res.status(200).json({ success: true, message: 'Brief submitted successfully' });
  } catch (err) {
    console.error('API Error:', err);
    return res.status(500).json({ error: err.message || 'Internal Server Error' });
  }
}
