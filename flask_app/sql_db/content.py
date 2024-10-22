class Content:
    def __init__(self, cursor=None):
        self.cursor = cursor
        self.date_format = '%Y/%m/%d'
    
    def get_by_id(self, id):
        query = """
            SELECT * FROM Content WHERE id = %s
        """

        self.cursor.execute(query, (id,)) # type: ignore
        return self.cursor.fetchall() # type: ignore
    
    def get_by_job_id(self, job_id):
        query = """
            SELECT * FROM Content WHERE job_id = %s
        """

        self.cursor.execute(query, (job_id,)) # type: ignore
        return self.cursor.fetchall() # type: ignore
    
    def get_by_user_id(self, user_id):
        query = """
            SELECT * FROM Content WHERE user_id = %s
        """

        self.cursor.execute(query, (user_id,)) # type: ignore
        return self.cursor.fetchall() # type: ignore

    def get_by_review_id(self, review_id):
        query = """
            SELECT * FROM Content WHERE review_id = %s
        """

        self.cursor.execute(query, (review_id,)) # type: ignore
        return self.cursor.fetchall() # type: ignore
    
    def get_by_job_and_user(self, user_id, job_id):
        query = """
            SELECT * FROM Content WHERE user_id = %s and job_id = %s
        """

        self.cursor.execute(query, (user_id, job_id)) # type: ignore
        return self.cursor.fetchall() # type: ignore
    
    def get_by_job_register_id(self, job_register_id):
        query = """
            SELECT * FROM Content WHERE job_register_id = %s
        """

        self.cursor.execute(query, (job_register_id,)) # type: ignore
        return self.cursor.fetchall() # type: ignore
    
    def get_by_job_register_id_and_user_id(self, job_register_id, user_id):
        query = """
            SELECT * FROM Content WHERE job_register_id = %s and user_id = %s
        """

        self.cursor.execute(query, (job_register_id, user_id)) # type: ignore
        return self.cursor.fetchall() # type: ignore

    def get_by_company(self, server_id):
        query = """
            SELECT * FROM Content WHERE server_id = %s and active = 1
        """

        self.cursor.execute(query, (server_id,)) # type: ignore
        return self.cursor.fetchall() # type: ignore
    
    def get_by_server(self):
        query = """
            SELECT * FROM Content WHERE active = 1
        """

        self.cursor.execute(query) # type: ignore
        return self.cursor.fetchall() # type: ignore

    def get_report_by_job_id(self, job_id: int):
        query = """
            SELECT user_id,
                COUNT(*) AS content_count,
                GROUP_CONCAT(link SEPARATOR ',') AS content_links,
                SUM(initial_plays) AS total_initial_plays,
                SUM(total_plays) AS total_total_plays,
                SUM(likes) AS total_likes,
                SUM(replays) AS total_replays,
                SUM(saves) AS total_saves,
                SUM(shares) AS total_shares,
                SUM(comments) AS total_comments,
                SUM(account_reach) AS total_account_reach,
                SUM(total_interactions) AS total_interactions,
                SUM(points) AS total_points,
                AVG(engagement_rate) AS avg_engagement_rate
            FROM Content
            WHERE job_id = %s
            GROUP BY user_id
        """

        self.cursor.execute(query, (job_id,))
        return self.cursor.fetchall()

    def get_all_by_job_id(self, job_ids: list):
        query = """
            SELECT * FROM Content WHERE job_id IN ({}) AND active = 1
        """
        placeholders = ','.join(['%s'] * len(job_ids))
        formatted_query = query.format(placeholders)
        self.cursor.execute(formatted_query, tuple(job_ids))

        return self.cursor.fetchall()

    def exist_by_social_type(self, job_register_id, social_type) -> bool:
        query = """
            SELECT 1 FROM Content WHERE job_register_id = %s AND social_type = %s
        """

        self.cursor.execute(query, (job_register_id, social_type)) # type: ignore
        return self.cursor.fetchone() is not None# type: ignore

    def create(self, job_register_id, job_id, user_id, review_id, server_id, content_type, link, ig_id, ig_content_id) -> bool:
        query = """
            INSERT INTO Content (job_register_id, job_id, user_id, review_id, server_id, type, link, ig_id, ig_content_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        self.cursor.execute(query, (job_register_id, job_id, user_id, review_id, server_id, content_type, link, ig_id, ig_content_id)) # type: ignore
        return True
    
    def update_link(self, review_id, link):
        update_query = "UPDATE Content SET "
        update_params = []

        if link is not None:
            update_query += "link = %s, "
            update_params.append(link)

        update_query = update_query.rstrip(", ") + " WHERE review_id = %s"
        update_params.append(review_id)
        self.cursor.execute(update_query, tuple(update_params)) # type: ignore

        return True
    
    def update_by_id(self, id, job_register_id=None, job_id=None, user_id=None, review_id=None, server_id=None, content_type=None, link=None, point=None, active=None) -> bool:
        update_query = "UPDATE Content SET "
        update_params = []

        if job_register_id is not None:
            update_query += "job_register_id = %s, "
            update_params.append(job_register_id)
        
        if job_id is not None:
            update_query += "job_id = %s, "
            update_params.append(job_id)
        
        if user_id is not None:
            update_query += "user_id = %s, "
            update_params.append(user_id)
        
        if review_id is not None:
            update_query += "review_id = %s, "
            update_params.append(review_id)

        if server_id is not None:
            update_query += "server_id = %s, "
            update_params.append(server_id)

        if content_type is not None:
            update_query += "type = %s, "
            update_params.append(content_type)

        if link is not None:
            update_query += "link = %s, "
            update_params.append(link)
        
        if point is not None:
            update_query += "point = %s, "
            update_params.append(point)

        if active is not None:
            update_query += "active = %s, "
            update_params.append(active)

        update_query = update_query.rstrip(", ") + " WHERE id = %s"
        update_params.append(id)
        self.cursor.execute(update_query, tuple(update_params)) # type: ignore
        self.cursor.fetchall() # type: ignore

        return True
    
    def update_active(self, id, active):
        update_query = "UPDATE Content SET "
        update_params = []

        if active is not None:
            update_query += "active = %s, "
            update_params.append(active)

        update_query = update_query.rstrip(", ") + " WHERE id = %s"
        update_params.append(id)
        self.cursor.execute(update_query, tuple(update_params)) # type: ignore
        self.cursor.fetchall() # type: ignore

        return True

    def update_status(self, id, initial_plays, total_plays, likes, replays, saves, shares, comments, account_reach, total_interactions, points, engagement, engagement_rate, shortcode, product_type, active) -> bool:
        update_query = "UPDATE Content SET "
        update_params = []

        if initial_plays is not None:
            update_query += "initial_plays = %s, "
            update_params.append(initial_plays)
        
        if total_plays is not None:
            update_query += "total_plays = %s, "
            update_params.append(total_plays)
        
        if likes is not None:
            update_query += "likes = %s, "
            update_params.append(likes)
        
        if replays is not None:
            update_query += "replays = %s, "
            update_params.append(replays)
        
        if saves is not None:
            update_query += "saves = %s, "
            update_params.append(saves)
        
        if shares is not None:
            update_query += "shares = %s, "
            update_params.append(shares)
        
        if comments is not None:
            update_query += "comments = %s, "
            update_params.append(comments)
        
        if account_reach is not None:
            update_query += "account_reach = %s, "
            update_params.append(account_reach)
        
        if total_interactions is not None:
            update_query += "total_interactions = %s, "
            update_params.append(total_interactions)

        if points is not None:
            update_query += "points = %s, "
            update_params.append(points)

        if engagement is not None:
            update_query += "engagement = %s, "
            update_params.append(engagement)
        
        if engagement_rate is not None:
            update_query += "engagement_rate = %s, "
            update_params.append(engagement_rate)
        
        if shortcode is not None:
            update_query += "shortcode = %s, "
            update_params.append(shortcode)
        
        if product_type is not None:
            update_query += "product_type = %s, "
            update_params.append(product_type)
        
        if active is not None:
            update_query += "active = %s, "
            update_params.append(active)

        update_query = update_query.rstrip(", ") + " WHERE id = %s"
        update_params.append(id)
        self.cursor.execute(update_query, tuple(update_params)) # type: ignore
        self.cursor.fetchall() # type: ignore

        return True

    def delete_by_job_register_id(self, job_register_id):
        delete_query = "DELETE FROM Content WHERE job_register_id = %s"
        self.cursor.execute(delete_query, (job_register_id)) # type: ignore

    def delete_by_link(self, job_register_id, link):
        delete_query = "DELETE FROM Content WHERE job_register_id = %s and link = %s"
        self.cursor.execute(delete_query, (job_register_id, link)) # type: ignore