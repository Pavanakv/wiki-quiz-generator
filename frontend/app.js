const API = "https://wiki-quiz-generator-sk32.onrender.com";

function openTab(tab) {
  document.querySelectorAll(".tab-content").forEach(t => t.classList.remove("active"));
  document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
  document.getElementById(tab).classList.add("active");

  if (tab === "history") loadHistory();
}

async function generateQuiz() {
  const url = document.getElementById("urlInput").value;
  const resBox = document.getElementById("result");

  if (!url) {
    resBox.innerHTML = "⚠️ Please enter a Wikipedia URL.";
    return;
  }

  resBox.innerHTML = "⏳ Generating quiz... Please wait.";

  try {
    const res = await fetch(`${API}/generate?url=${encodeURIComponent(url)}`, {
      method: "POST"
    });

    const data = await res.json();
    console.log("API RESPONSE:", data);

    if (data.error) {
      resBox.innerHTML = "❌ Gemini quota exceeded. Please view history tab.";
      return;
    }

    if (!data.quiz || !data.quiz.quiz) {
      resBox.innerHTML = "❌ Invalid quiz format received.";
      return;
    }

    renderQuiz(data.quiz);

  } catch (err) {
    console.error(err);
    resBox.innerHTML = "❌ Backend not responding.";
  }
}

function renderQuiz(data, containerId = "result") {
  const resBox = document.getElementById(containerId);

  let html = `<h2>Quiz</h2>`;

  data.quiz.forEach((q, index) => {
    html += `
      <div class="quiz-card">
        <h3>Q${index + 1}. ${q.question}</h3>
        <ul>
          ${q.options.map(o => `<li>${o}</li>`).join("")}
        </ul>
        <p><b>Answer:</b> ${q.correct_answer}</p>
        <p><b>Difficulty:</b> ${q.difficulty}</p>
        <p><b>Explanation:</b> ${q.explanation}</p>
      </div>
    `;
    html += `<div class="related-box"><b>Related Topics:</b> ${data.related_topics.join(", ")}</div>`;
  });


  html += `<p><b>Related Topics:</b> ${data.related_topics.join(", ")}</p>`;

  resBox.innerHTML = html;
}


// ---------------- HISTORY ----------------

async function loadHistory() {
  const table = document.getElementById("historyTable");
  table.innerHTML = "<tr><td colspan='4'>Loading...</td></tr>";

  const res = await fetch(`${API}/history`);
  const data = await res.json();

  table.innerHTML = "";

  data.forEach(q => {
    table.innerHTML += `
      <tr>
        <td>${q.id}</td>
        <td>${q.url}</td>
        <td>${new Date(q.created_at).toLocaleString()}</td>
        <td><button onclick="viewQuiz(${q.id})">View</button></td>
      </tr>
    `;
  });
}

async function viewQuiz(id) {
  const res = await fetch(`${API}/history/${id}`);
  const data = await res.json();

  document.getElementById("modal").style.display = "block";

  renderQuiz(data.quiz, "modalBody");
}

function closeModal() {
  document.getElementById("modal").style.display = "none";
}
