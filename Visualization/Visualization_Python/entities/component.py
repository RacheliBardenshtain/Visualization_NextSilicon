from typing import Optional


class Component:
    _id_counter = 0  # Static variable to keep track of IDs

    def __init__(self, id: Optional[int] = None, type_name: Optional[str] = None):
        # If no ID is sent it will be initialized as an automatic number
        if id is None:
            Component._id_counter += 1
            self.id = Component._id_counter
        else:
            self.id = id
        self.type_name = type_name
        self.active_logs = []
    
    def get_attribute_from_active_logs(self,attribute):
        if len(self.active_logs) > 0:
            attributes = []
            for log in self.active_logs:
                attributes.append(getattr(log, attribute))
            return attributes
        return []
