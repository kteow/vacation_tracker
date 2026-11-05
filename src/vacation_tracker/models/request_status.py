from dataclasses import dataclass

@dataclass
class RequestStatus:
    request_status_id: int
    status: str