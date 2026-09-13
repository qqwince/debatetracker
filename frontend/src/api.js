const API = "/api/v1";

function authHeaders(login) {
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${login}`,
  };
}

async function parseError(res) {
  const text = await res.text();
  try {
    const data = JSON.parse(text);
    if (typeof data.detail === "string") return data.detail;
    if (Array.isArray(data.detail)) {
      return data.detail.map((item) => item.msg || JSON.stringify(item)).join("; ");
    }
    return text || res.statusText;
  } catch {
    return text || res.statusText;
  }
}

export async function createUser(login) {
  const res = await fetch(`${API}/users`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ login }),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function getMe(login) {
  const res = await fetch(`${API}/users/me`, {
    headers: authHeaders(login),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function createGame(login, payload) {
  const res = await fetch(`${API}/game`, {
    method: "POST",
    headers: authHeaders(login),
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}
