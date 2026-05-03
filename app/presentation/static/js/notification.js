(function () {
    console.log("Notification script loaded");
  const notifList = document.querySelector(".notif-list");
  const notifBadge = document.getElementById("notif-count");

  let unreadCount = 0;

  function getCookie(name) {
    return document.cookie
      .split("; ")
      .find(row => row.startsWith(name + "="))
      ?.split("=")[1];
  }

  function addNotification(message, createdAt) {
    // Supprimer le message "vide" s'il existe
    const empty = notifList.querySelector(".notif-empty");
    if (empty) empty.remove();

    const item = document.createElement("div");
    item.className = "notification-item";

    item.innerHTML = `
      <div class="notification-content">
        <div class="icon-wrapper"></div>

        <div class="notification-details">
          <div class="notification-header">
            <span class="notification-title">Library</span>
            <span class="notification-time">
              ${new Date(createdAt).toLocaleTimeString()}
            </span>
          </div>

          <p class="notification-text">
            ${message}
          </p>
        </div>
      </div>
    `;

    notifList.prepend(item);

    unreadCount++;
    notifBadge.textContent = unreadCount;
    notifBadge.style.display = "block";
  }

  // --- WebSocket ---
  const token = getCookie("access_token");
  if (!token) return;

  const ws = new WebSocket(
    `ws://${window.location.host}/ws/notifications?token=${token}`
  );

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.type !== "notification") return;

    addNotification(
      data.notification.message,
      data.notification.created_at
    );
  };

  ws.onopen = () => {
    console.log("[WS] Notifications connected");
  };

  ws.onclose = () => {
    console.log("[WS] Notifications disconnected");
  };

})();

