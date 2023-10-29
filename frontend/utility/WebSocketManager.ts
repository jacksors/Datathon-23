class WebSocketManager {
  private ws: WebSocket;
  private onMessageCallback: (message: any) => void;

  constructor(url: string, onMessageCallback: (message: any) => void) {
    this.ws = new WebSocket(url);
    this.onMessageCallback = onMessageCallback;

    this.ws.onopen = () => {
      console.log("WebSocket is open");
    };

    this.ws.onerror = (error) => {
      console.log("WebSocket error:", error);
    };

    this.ws.onclose = () => {
      console.log("WebSocket is closed");
    };

    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.handleMessage(message);
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

  saveStroke(name: string) {
    if (this.ws.readyState === WebSocket.OPEN) {
      const message = JSON.stringify({save: true, name: name });
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

  private handleMessage(message: any) {
    this.onMessageCallback(message);
  }
}

export default WebSocketManager;
