"""Import this library to use connect manager."""

from .manager import ConnectManager

connect_manager = ConnectManager()
get_controller = connect_manager.get_controller
