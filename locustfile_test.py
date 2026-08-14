import random
from locust import HttpUser, task, between

class DummyJsonUser(HttpUser):
    wait_time = between(1, 5)

    @task(3)
    def get_all_posts(self):
        self.client.get("/posts")

    @task(2)
    def get_single_post(self):
        post_id = random.randint(1, 100)
        self.client.get(f"/posts/{post_id}", name="/posts/[id]")

    @task(1)
    def get_comments_by_post(self):
        post_id = random.randint(1, 100)
        self.client.get(f"/comments?postId={post_id}", name="/comments?postId=[id]")
    