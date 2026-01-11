"""
AI Content Generation Service
Mock implementation with platform-specific content generation
"""
import random


class ContentGenerator:
    """Service for generating social media content"""
    
    def __init__(self):
        self.platforms = ['instagram', 'tiktok', 'facebook', 'youtube', 'snapchat']
        
        # Mock image URLs from Unsplash
        self.sample_images = [
            'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800',  # Burger
            'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800',  # Salad
            'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800',  # Pizza
            'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=800',  # Pancakes
            'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800',  # Food spread
            'https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=800',  # Eggs
            'https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=800',  # Pasta
            'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800',  # Steak
        ]
    
    def generate_content(self, platform, content_type, topic=''):
        """Generate content for a specific platform"""
        
        if platform not in self.platforms:
            raise ValueError(f"Unsupported platform: {platform}")
        
        # Get DARA's competitive analysis
        dara_insight = self._generate_dara_insight(platform)
        
        # Generate platform-specific content
        if platform == 'instagram':
            content = self._generate_instagram_content(content_type, topic)
        elif platform == 'tiktok':
            content = self._generate_tiktok_content(content_type, topic)
        elif platform == 'facebook':
            content = self._generate_facebook_content(content_type, topic)
        elif platform == 'youtube':
            content = self._generate_youtube_content(content_type, topic)
        elif platform == 'snapchat':
            content = self._generate_snapchat_content(content_type, topic)
        else:
            content = self._generate_generic_content(topic)
        
        # Calculate VERA's viral score
        viral_score = self._calculate_viral_score(content, platform)
        
        content.update({
            'dara_insight': dara_insight,
            'viral_score': viral_score
        })
        
        return content
    
    def generate_custom_content(self, platform, user_input):
        """Generate custom content from user voice/text input"""
        
        # In real implementation, would use NLP to parse user input
        # and generate relevant content
        
        dara_insight = self._generate_dara_insight(platform)
        
        content = {
            'caption': f"Custom content based on: {user_input}\n\nComing soon to our restaurant! 🍽️✨",
            'hashtags': '#Custom #NewItem #ComingSoon #FoodLover',
            'image_url': random.choice(self.sample_images),
            'dara_insight': dara_insight,
            'viral_score': random.randint(70, 90)
        }
        
        return content
    
    def _generate_dara_insight(self, platform):
        """Generate DARA's competitive analysis insight"""
        
        competitors = ['Luigi\'s Pizza', 'Bella Vista', 'Tony\'s Bistro', 'The Food House']
        trends = [
            'close-up food shots getting 2.3x engagement',
            'nostalgia-themed content trending locally',
            'behind-the-scenes content showing 34% higher retention',
            'customer testimonial posts performing well',
            'time-lapse cooking videos seeing high reach'
        ]
        
        competitor = random.choice(competitors)
        trend = random.choice(trends)
        
        insights = [
            f"{competitor} got {random.randint(8, 20)}k likes with similar content yesterday. {trend.capitalize()}.",
            f"Trending in local area: {trend}. {competitor} leading with this format.",
            f"{competitor}'s recent post hit {random.randint(15, 50)}k views. Consider: {trend}.",
            f"Analysis shows {trend}. {competitor} capitalizing on this trend effectively."
        ]
        
        return random.choice(insights)
    
    def _calculate_viral_score(self, content, platform):
        """Calculate VERA's viral potential score"""
        
        # Mock scoring based on content attributes
        base_score = random.randint(70, 95)
        
        # Bonus for hashtags
        if content.get('hashtags'):
            base_score += random.randint(0, 5)
        
        # Platform-specific adjustments
        if platform == 'tiktok' and 'trending' in content.get('caption', '').lower():
            base_score += 5
        
        return min(base_score, 99)
    
    def _generate_instagram_content(self, content_type, topic):
        """Generate Instagram-specific content"""
        
        captions = {
            'post': [
                f"Remember your first burger with Dad? That feeling never gets old. 🍔❤️\n\n#ComfortFood #FamilyMoments #BurgerLove #FoodMemories #{topic}",
                f"Sunday brunch hits different when it's made with love. ☀️🥞\n\n#BrunchGoals #WeekendVibes #FoodieLife #{topic}",
                f"That golden hour glow + our signature dish = perfection ✨🍽️\n\n#FoodPhotography #InstaFood #Delicious #{topic}"
            ],
            'story': [
                "Behind the scenes in our kitchen right now 👨‍🍳🔥\n\nSwipe up to order!",
                "LIVE: Chef preparing tonight's special 🎬✨",
                "Guess what's cooking? 🤔👀 (Hint: It's amazing)"
            ],
            'reel': [
                f"POV: You just walked into heaven 😍🍕\n\n#Reels #FoodPorn #PizzaLover #Satisfying #{topic}",
                f"The cheese pull that broke the internet 🧀🤤\n\n#FoodReels #Satisfying #CheeseLovers #{topic}"
            ]
        }
        
        return {
            'caption': random.choice(captions.get(content_type, captions['post'])),
            'hashtags': '#InstagramFood #FoodLover #Delicious',
            'image_url': random.choice(self.sample_images)
        }
    
    def _generate_tiktok_content(self, content_type, topic):
        """Generate TikTok-specific content"""
        
        captions = [
            f"When the cheese pull hits different 🧀😮‍💨 #FoodTok #CheesePull #SatisfyingVideo #FoodASMR #{topic}",
            f"Making our famous burger cause why not 💅🍔 #Trending #BurgerTok #{topic}",
            f"POV: You're about to have the best meal of your life 😋 #POV #FoodTikTok #{topic}"
        ]
        
        return {
            'caption': random.choice(captions),
            'hashtags': '#FoodTok #Viral #Trending',
            'image_url': random.choice(self.sample_images),
            'video_url': 'https://example.com/video-concept.mp4'
        }
    
    def _generate_facebook_content(self, content_type, topic):
        """Generate Facebook-specific content"""
        
        captions = [
            f"🍔 FAMILY SPECIAL THIS WEEK 🍔\n\nBring the whole family! Kids eat free on Tuesdays.\n\nReservations: (555) 123-4567\n📍 123 Main Street\n\n#{topic}",
            f"Join us for a memorable dining experience! Perfect for date nights, family gatherings, or just because. 🍽️\n\nBook now: Link in bio\n\n#{topic}"
        ]
        
        return {
            'caption': random.choice(captions),
            'hashtags': '#FamilyDining #LocalRestaurant',
            'image_url': random.choice(self.sample_images)
        }
    
    def _generate_youtube_content(self, content_type, topic):
        """Generate YouTube-specific content"""
        
        if content_type == 'short':
            caption = f"The secret to our perfect medium-rare steak 🥩🔥\n\n#Shorts #Cooking #SteakTok #ChefTips #{topic}"
        else:
            caption = f"FULL RECIPE: How We Make Our Signature Burger From Scratch\n\nIngredients in description! 🍔👨‍🍳\n\n#{topic}"
        
        return {
            'caption': caption,
            'hashtags': '#YouTubeCooking #Recipe #FoodVideo',
            'video_url': 'https://example.com/youtube-video.mp4'
        }
    
    def _generate_snapchat_content(self, content_type, topic):
        """Generate Snapchat-specific content"""
        
        captions = [
            "Order now through the link! Fresh out the oven 🔥",
            "Behind the scenes: lunch rush edition 🏃‍♂️💨",
            "What should we make next? Vote now! 🗳️👀"
        ]
        
        return {
            'caption': random.choice(captions),
            'hashtags': '#Snap #FoodSnap',
            'image_url': random.choice(self.sample_images)
        }
    
    def _generate_generic_content(self, topic):
        """Generate generic content"""
        
        return {
            'caption': f"Check out our latest! {topic} 🍽️✨\n\n#Food #Restaurant #Delicious",
            'hashtags': '#Food #Yum',
            'image_url': random.choice(self.sample_images)
        }
