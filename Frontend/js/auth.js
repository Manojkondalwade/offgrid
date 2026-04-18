// OffGrid auth/session helpers
(function () {
  const TOKEN_KEY = 'offgrid.token';
  const USER_KEY = 'offgrid.user';

  function safeParse(value) {
    try {
      return value ? JSON.parse(value) : null;
    } catch (_) {
      return null;
    }
  }

  function getToken() {
    return localStorage.getItem(TOKEN_KEY);
  }

  function getUser() {
    return safeParse(localStorage.getItem(USER_KEY));
  }

  function setSession(token, user) {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  function clearSession() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  }

  function signOut(redirectTo = 'login.html') {
    clearSession();
    window.location.href = redirectTo;
  }

  function requireRole(role, redirectTo = 'login.html') {
    const token = getToken();
    const user = getUser();
    if (!token || !user || (role && user.role !== role)) {
      clearSession();
      window.location.href = redirectTo;
      return false;
    }
    return true;
  }

  async function authorizedFetch(url, options = {}) {
    const token = getToken();
    const headers = {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`
    };

    if (options.body && !headers['Content-Type']) {
      headers['Content-Type'] = 'application/json';
    }

    const response = await fetch(url, { ...options, headers });
    if (response.status === 401 || response.status === 422) {
      clearSession();
    }
    return response;
  }

  window.OffGridAuth = {
    getToken,
    getUser,
    setSession,
    clearSession,
    signOut,
    requireRole,
    authorizedFetch
  };
})();
