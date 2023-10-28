class WebSocketManager {
  private ws: WebSocket;

  constructor(url: string) {
    this.ws = new WebSocket(url);

    this.ws.onopen = () => {
      console.log("WebSocket is open");
    };

    this.ws.onerror = (error) => {
      console.log("WebSocket error:", error);
    };

    this.ws.onclose = () => {
      console.log("WebSocket is closed");
    };
  }

  sendStroke(stroke: { xs: number[]; ys: number[] }) {
    if (this.ws.readyState === WebSocket.OPEN) {
      const message = JSON.stringify(stroke);
      this.ws.send(message);
    } else {
      console.log("WebSocket is not open. Cannot send message.");
    }
  }

  sendClear() {
    if (this.ws.readyState === WebSocket.OPEN) {
      const message = JSON.stringify({ clear: true });
      this.ws.send(message);
    } else {
      console.log("WebSocket is not open. Cannot send message.");
    }
  }
}

export default WebSocketManager;
