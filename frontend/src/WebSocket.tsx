import React, { createContext, use, useEffect, useState } from "react";

interface IWebsocketContext {
  ws: WebSocket | null;
}

const WebsocketContext = createContext<IWebsocketContext>({
  ws: null,
});

const WebsocketProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [ws, setWS] = useState<WebSocket | null>(null);
  useEffect(() => {
    setWS(new WebSocket(`ws://localhost:8000/task/ws`));
  }, []);
  return (
    <React.Fragment>
      <WebsocketContext.Provider value={{ ws }}>
        {children}
      </WebsocketContext.Provider>
    </React.Fragment>
  );
};

export default WebsocketProvider;

export const useWebsocket = () => {
  const context = use(WebsocketContext);
  if (!context) {
    throw new Error("useWebsocket must be used inside WebsocketProvider");
  }
  return context;
};
