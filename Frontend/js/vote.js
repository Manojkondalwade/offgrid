// vote.js — Time-slot poll logic

const pollState = {};

function selectSlot(el, pollId, slotIndex, pct) {
  const poll = el.closest('.poll-card');
  poll.querySelectorAll('.slot-option').forEach(s => s.classList.remove('selected'));
  el.classList.add('selected');
  if (!pollState[pollId]) pollState[pollId] = {};
  pollState[pollId].selected = slotIndex;
}

function submitVote(pollId) {
  if (!pollState[pollId] || pollState[pollId].selected === undefined) {
    showToast('Please select a time slot first.', 'warn');
    return;
  }
  const poll = document.getElementById(pollId);
  const slots = poll.querySelectorAll('.slot-option');
  slots.forEach(s => { s.onclick = null; s.style.cursor = 'default'; });
  const submitBtn = poll.querySelector('.btn-primary');
  submitBtn.textContent = '✅ Voted!';
  submitBtn.disabled = true;
  submitBtn.style.background = 'var(--green-dim)';
  submitBtn.style.color = 'var(--green)';
  showToast('Vote submitted! Results updated.', 'success');
}

function showToast(msg, type) {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = 'toast';
  const icon = type === 'success' ? '✅' : type === 'warn' ? '⚠️' : 'ℹ️';
  toast.innerHTML = `<span>${icon}</span><span style="font-size:0.875rem;">${msg}</span>`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3500);
}