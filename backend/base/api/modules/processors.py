
class RunProcessor():
    
    def __init__(self, run_id=None):
        self.run_id = run_id
        
    def get_next_slide(self):
        
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def get_next_hint(self):
        
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def send_answer(self):
        
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def create_run(self):
        
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def get_or_create(self):
        configs_processor = ConfigProcessor()
        max_slides_per_run = configs_processor.get_config('max_slides_per_run')
        
        new_run = run_processor.create_run(
            id_user= request.user.id,
            current_hint= first_hint.id,
            slides_left= max_slides_per_run
        )
        
        return NotImplementedError("This method should be overridden by subclasses.")
    
    def _get_run(self):
        
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def _get_random_slide(self):
        
        raise NotImplementedError("This method should be overridden by subclasses.")