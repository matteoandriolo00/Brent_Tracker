import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  Bell,
  LayoutDashboard,
  LogOut,
  Plus,
  Trash2,
  TrendingDown,
  TrendingUp,
  User,
} from "lucide-react";
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { api } from "./api";

function getUserIdFromToken(token) {
  const match = token?.match(/token_fittizio_per_(\d+)/);
  return match ? Number(match[1]) : null;
}

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [authMode, setAuthMode] = useState("login");

  const userId = getUserIdFromToken(token);

  if (!token || !userId) {
    return (
      <AuthPage
        mode={authMode}
        onModeChange={setAuthMode}
        onLogin={(newToken) => {
          localStorage.setItem("token", newToken);
          setToken(newToken);
        }}
      />
    );
  }

  return (
    <Dashboard
      userId={userId}
      onLogout={() => {
        localStorage.removeItem("token");
        setToken(null);
      }}
    />
  );
}

function AuthPage({ mode, onModeChange, onLogin }) {
  const [form, setForm] = useState({
    email: "",
    username: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const isLogin = mode === "login";

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (isLogin) {
        const result = await api.login({
          username: form.username,
          password: form.password,
        });
        onLogin(result.access_token);
      } else {
        await api.register({
          email: form.email,
          username: form.username || null,
          password: form.password,
        });

        const result = await api.login({
          username: form.username,
          password: form.password,
        });
        onLogin(result.access_token);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-card">
        <div className="brand brand-centered">
          <div className="brand-icon">
            <Activity size={22} />
          </div>
          <div>
            <strong>Brent Tracker</strong>
            <span>Market dashboard</span>
          </div>
        </div>

        <div className="auth-heading">
          <h1>{isLogin ? "Bentornato." : "Crea il tuo account."}</h1>
          <p>
            {isLogin
              ? "Accedi per controllare il prezzo del Brent."
              : "Inizia a monitorare il mercato."}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          {!isLogin && (
            <label>
              Email
              <input
                type="email"
                required
                value={form.email}
                onChange={(e) =>
                  setForm({ ...form, email: e.target.value })
                }
              />
            </label>
          )}

          <label>
            Username
            <input
              required
              value={form.username}
              onChange={(e) =>
                setForm({ ...form, username: e.target.value })
              }
            />
          </label>

          <label>
            Password
            <input
              type="password"
              required
              value={form.password}
              onChange={(e) =>
                setForm({ ...form, password: e.target.value })
              }
            />
          </label>

          {error && <div className="error">{error}</div>}

          <button className="primary-button" disabled={loading}>
            {loading
              ? "Attendi..."
              : isLogin
                ? "Accedi"
                : "Registrati"}
          </button>
        </form>

        <button
          className="switch-auth"
          onClick={() => {
            setError("");
            onModeChange(isLogin ? "register" : "login");
          }}
        >
          {isLogin
            ? "Non hai un account? Registrati"
            : "Hai già un account? Accedi"}
        </button>
      </section>
    </main>
  );
}

function Dashboard({ userId, onLogout }) {
  const [page, setPage] = useState("dashboard");
  const [price, setPrice] = useState(null);
  const [history, setHistory] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [error, setError] = useState("");
  const [refreshing, setRefreshing] = useState(false);

  async function loadData() {
    setError("");
    setRefreshing(true);

    try {
      const [current, historyResult, alertsResult] = await Promise.all([
        api.getCurrentPrice(),
        api.getHistory(),
        api.getAlerts(userId),
      ]);

      setPrice(current.data);
      setHistory(historyResult.data);
      setAlerts(alertsResult);
    } catch (err) {
      setError(err.message);
    } finally {
      setRefreshing(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function createAlert(data) {
    try {
      await api.createAlert({ ...data, user_id: userId });
      await loadData();
      setPage("alerts");
    } catch (err) {
      setError(err.message);
    }
  }

  async function toggleAlert(alert) {
    try {
      await api.updateAlertStatus(
        alert.id,
        alert.status === "ACTIVE" ? "INACTIVE" : "ACTIVE"
      );
      await loadData();
    } catch (err) {
      setError(err.message);
    }
  }

  async function deleteAlert(alertId) {
    try {
      await api.deleteAlert(alertId);
      await loadData();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleDeleteAccount() {
    const username = window.prompt("Inserisci il tuo username per confermare l'eliminazione dell'account:");
    if (!username) return;

    try {
      await api.deleteUser(username);
      alert("Account eliminato con successo.");
      onLogout(); // Disconnette l'utente e lo rimanda al login
    } catch (err) {
      alert("Errore durante l'eliminazione: " + err.message);
    }
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <Activity size={22} />
          </div>
          <div>
            <strong>Brent Tracker</strong>
            <span>Market dashboard</span>
          </div>
        </div>

        <nav>
          <button
            className={page === "dashboard" ? "nav-item active" : "nav-item"}
            onClick={() => setPage("dashboard")}
          >
            <LayoutDashboard size={18} />
            Dashboard
          </button>

          <button
            className={page === "alerts" ? "nav-item active" : "nav-item"}
            onClick={() => setPage("alerts")}
          >
            <Bell size={18} />
            I miei alert
          </button>
        </nav>

        <div className="sidebar-bottom">
          <div className="user-box">
            <div className="avatar">
              <User size={17} />
            </div>
            <div>
              <strong>Utente #{userId}</strong>
              <span>Account attivo</span>
            </div>
          </div>

          <button className="logout-button" onClick={onLogout}>
            <LogOut size={17} />
            Esci
          </button>

          
          <button className="logout-button" style={{ color: '#ef4444', marginTop: '10px' }} onClick={handleDeleteAccount}>
            <Trash2 size={17} />
            Elimina Account
          </button>


        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="eyebrow">MARKET OVERVIEW</p>
            <h1>{page === "dashboard" ? "Dashboard" : "I miei alert"}</h1>
          </div>

          <button className="refresh-button" onClick={loadData}>
            {refreshing ? "Aggiornamento..." : "Aggiorna dati"}
          </button>
        </header>

        {error && <div className="error global-error">{error}</div>}

        {page === "dashboard" ? (
          <DashboardPage
            price={price}
            history={history}
            alerts={alerts}
            onNewAlert={() => setPage("new-alert")}
          />
        ) : page === "alerts" ? (
          <AlertsPage
            alerts={alerts}
            onNewAlert={() => setPage("new-alert")}
            onToggle={toggleAlert}
            onDelete={deleteAlert}
          />
        ) : (
          <NewAlertPage
            onCancel={() => setPage("alerts")}
            onCreate={createAlert}
          />
        )}
      </main>
    </div>
  );
}

function DashboardPage({ price, history, alerts, onNewAlert }) {
  const chartData = useMemo(
    () =>
      history.map((item) => ({
        ...item,
        time: new Date(item.timestamp).toLocaleDateString("it-IT", {
          day: "2-digit",
          month: "2-digit",
        }),
      })),
    [history]
  );

  const activeAlerts = alerts.filter((alert) => alert.status === "ACTIVE");

  return (
    <div className="page-content">
      <section className="stats-grid">
        <div className="stat-card featured">
          <div className="stat-label">PREZZO BRENT</div>
          <div className="price-value">
            {price ? `$${price.price.toFixed(2)}` : "—"}
          </div>
          <span className="stat-subtitle">Ultimo valore disponibile</span>
        </div>

        <div className="stat-card">
          <div className="stat-label">ALERT ATTIVI</div>
          <div className="stat-number">{activeAlerts.length}</div>
          <span className="stat-subtitle">Monitoraggio automatico</span>
        </div>

        <div className="stat-card">
          <div className="stat-label">DATI STORICI</div>
          <div className="stat-number">{history.length}</div>
          <span className="stat-subtitle">Prezzi salvati</span>
        </div>
      </section>

      <section className="content-grid">
        <div className="panel chart-panel">
          <div className="panel-heading">
            <div>
              <h2>Andamento del Brent</h2>
              <p>Storico dei prezzi salvati</p>
            </div>
            <TrendingUp size={20} />
          </div>

          <div className="chart">
            {chartData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData}>
                  <CartesianGrid vertical={false} />
                  <XAxis dataKey="time" />
                  <YAxis domain={["auto", "auto"]} />
                  <Tooltip />
                  <Area
                    type="monotone"
                    dataKey="price"
                    strokeWidth={2}
                    fillOpacity={0.12}
                  />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div className="empty-state">Nessun dato storico disponibile.</div>
            )}
          </div>
        </div>

        <div className="panel">
          <div className="panel-heading">
            <div>
              <h2>Alert recenti</h2>
              <p>Le tue soglie di prezzo</p>
            </div>
            <Bell size={20} />
          </div>

          <AlertsList
            alerts={alerts.slice(0, 5)}
            compact
            onToggle={() => {}}
            onDelete={() => {}}
          />

          <button className="secondary-button full-width" onClick={onNewAlert}>
            <Plus size={17} />
            Crea nuovo alert
          </button>
        </div>
      </section>
    </div>
  );
}

function AlertsPage({ alerts, onNewAlert, onToggle, onDelete }) {
  return (
    <div className="page-content">
      <div className="page-actions">
        <p>Gestisci le soglie che vuoi monitorare.</p>
        <button className="primary-button small" onClick={onNewAlert}>
          <Plus size={17} />
          Nuovo alert
        </button>
      </div>

      <div className="panel">
        <AlertsList
          alerts={alerts}
          onToggle={onToggle}
          onDelete={onDelete}
        />
      </div>
    </div>
  );
}

function AlertsList({ alerts, compact = false, onToggle, onDelete }) {
  if (alerts.length === 0) {
    return (
      <div className="empty-state">
        <Bell size={28} />
        <p>Non hai ancora creato alert.</p>
      </div>
    );
  }

  return (
    <div className="alerts-list">
      {alerts.map((alert) => (
        <div className="alert-row" key={alert.id}>
          <div className="alert-direction">
            {alert.direction === "ABOVE" ? (
              <TrendingUp size={18} />
            ) : (
              <TrendingDown size={18} />
            )}
          </div>

          <div className="alert-info">
            <strong>
              {alert.direction === "ABOVE" ? "Sopra" : "Sotto"} $
              {alert.target_price.toFixed(2)}
            </strong>
            <span>Alert #{alert.id}</span>
          </div>

          <span
            className={
              alert.status === "ACTIVE"
                ? "status active-status"
                : "status inactive-status"
            }
          >
            {alert.status}
          </span>

          {!compact && (
            <>
              <button
                className="icon-button"
                title="Attiva/disattiva"
                onClick={() => onToggle(alert)}
              >
                <Bell size={17} />
              </button>
              <button
                className="icon-button danger"
                title="Elimina"
                onClick={() => onDelete(alert.id)}
              >
                <Trash2 size={17} />
              </button>
            </>
          )}
        </div>
      ))}
    </div>
  );
}

function NewAlertPage({ onCancel, onCreate }) {
  const [targetPrice, setTargetPrice] = useState("");
  const [direction, setDirection] = useState("ABOVE");

  function handleSubmit(event) {
    event.preventDefault();

    onCreate({
      target_price: Number(targetPrice),
      direction,
    });
  }

  return (
    <div className="page-content">
      <div className="panel form-panel">
        <div className="panel-heading">
          <div>
            <h2>Nuovo alert</h2>
            <p>Ricevi un alert quando il prezzo raggiunge la soglia.</p>
          </div>
          <Bell size={20} />
        </div>

        <form onSubmit={handleSubmit} className="alert-form">
          <label>
            Prezzo target
            <input
              type="number"
              step="0.01"
              min="0"
              required
              placeholder="Es. 80.00"
              value={targetPrice}
              onChange={(e) => setTargetPrice(e.target.value)}
            />
          </label>

          <label>
            Direzione
            <select
              value={direction}
              onChange={(e) => setDirection(e.target.value)}
            >
              <option value="ABOVE">Sopra il prezzo</option>
              <option value="BELOW">Sotto il prezzo</option>
            </select>
          </label>

          <div className="form-actions">
            <button type="button" className="secondary-button" onClick={onCancel}>
              Annulla
            </button>
            <button type="submit" className="primary-button">
              Crea alert
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;