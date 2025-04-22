class MessageHandler:
    @staticmethod
    def create_response(
        log: setResponseLog = None,
        code: setResponseCode = None,
        command: setResponseCommand = None,
    ):
        """
        Create a standardized response with logging

        Args:
            logs (Logs, optional): Existing logs object
            code (Code, optional): Code object
            commands (Commands, optional): Commands object

        Returns:
            Dict containing response details with logging
        """
        try:
            server_log = ServerEventLogger().log_request(
                request_path="/api/response",
                method="POST",
                request_data={
                    "has_logs": log is not None,
                    "has_code": code is not None,
                    "has_commands": command is not None,
                },
                status_code=200,
            )
            if log is None:
                log = setResponseLog(server_log=server_log)
            else:
                log.server_log = server_log

            return {
                "logs": log.to_dict(),
                "code": code.to_dict() if code else None,
                "commands": command.to_dict() if command else None,
            }
        except Exception as e:
            error_log = ServerEventLogger().log_error(
                "Failed to create response",
                exception=e,
                context={
                    "has_logs": log is not None,
                    "has_code": code is not None,
                    "has_commands": command is not None,
                },
            )

            return {
                "logs": setResponseLog(server_log=error_log).to_dict(),
                "error": str(e),
                "done": False,
            }


async def broadcast(self, message: dict):
    disconnected_clients = []
    for connection in self.active_connections:
        try:
            if connection.client_state != "closed":
                await connection.send_text(json.dumps(message))
        except Exception as e:
            print(f"Error broadcasting to client: {e}")
            disconnected_clients.append(connection)

    for client in disconnected_clients:
        self.disconnect(client)
