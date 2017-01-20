"""
    This module manages the blog features.
    Allow users creates/edit/remove posts.
    Allow users creates/edit/remove comments
    from a post.
    Allow users like/unlike posts.
"""
import json
from common.database import Comment
from common.database import Post
from common.request import BlogHandler
from common.request import Page

class WelcomeHandler(BlogHandler):
    """ List ten most recent posts. """

    def __init__(self, request, response):
        """ add post id """
        super(WelcomeHandler, self).__init__(request, response)
        self.post_id = None

    def render_post_form(self, error="", content="", subject=""):
        """ Render form to create/edit posts. """
        self.render('post_form.html',
                    page=self,
                    error=error,
                    subject=subject,
                    content=content)

    def get_page_stack(self):
        """
            Stack of current page label and url.
            Used to create a navigation component.
        """
        return [Page(label='Home', url='/blog')]

    def get(self):
        """ render /GET /blog """
        if self.is_user_authenticated():
            posts = Post.get_most_recent()
            self.render('welcome.html', page=self, posts=posts)

    def is_owner(self, post):
        """
            return True if the user is the
            owner of the post, otherwise
            returns false
         """
        return post.author.key().id() == self.user.key().id()

class NewPostHandler(WelcomeHandler):
    """ Create a new post. """

    def get_page_stack(self):
        """
            Stack of current page label and url.
            Used to create a navigation component.
        """
        pages = super(NewPostHandler, self).get_page_stack()
        pages.append(Page(label='New Post', url='/blog/newpost'))
        return pages

    def get(self):
        """
            handle /GET /blog/<blog_id> operation
            and render post form
        """
        if self.is_user_authenticated():
            self.render_post_form()

    def post(self):
        """
            handle /POST /blog/<blog_id> operation
            and render post form if error,
            otherwise redirect to post detail
        """
        if self.is_user_authenticated():
            subject = self.request.POST['subject']
            content = self.request.POST['content']

            if subject and content:
                post = Post.register(subject=subject,
                                     content=content,
                                     author=self.user)
                post_id = post.key().id()
                post_url = "/blog/%s" % post_id
                self.redirect(post_url, permanent=True)
            else:
                error = 'subject and content, please!'
                self.render_post_form(error=error,
                                      subject=subject,
                                      content=content)

class EditPostHandler(WelcomeHandler):
    """ Edit a existing post. """

    def get_page_stack(self):
        """
            Stack of current page label and url.
            Used to create a navigation component.
        """
        pages = super(EditPostHandler, self).get_page_stack()
        pages.append(Page(label='Edit Post',
                          url='/blog/edit/%s' % self.post_id))
        return pages

    def get(self, post_id):
        """
            Handle /GET /blog/<blog_id> operation
            and render post form for edit an existing
            post. If the post does not exist, redirect
            user to the post list (welcome page).
        """
        if self.is_user_authenticated():
            self.post_id = post_id
            post = Post.by_id(int(post_id))

            if not post:
                self.redirect("/blog", permanent=True)
            else:
                self.render_post_form(subject=post.subject,
                                      content=post.content)

    def post(self, post_id):
        """
            handle /POST /blog/<blog_id> operation
            and render post form if there is any error.
            Otherwise redirect to welcome page.
        """
        if self.is_user_authenticated():
            self.post_id = post_id
            subject = self.request.POST['subject']
            content = self.request.POST['content']

            if not post_id and not post_id.isdigit():
                self.redirect("/blog", permanent=True)
            elif not (subject and content):
                error = 'subject and content, please!'
                self.render_post_form(error=error,
                                      subject=subject,
                                      content=content)
            else:
                self.post_id = post_id
                post = Post.by_id(int(post_id))

                if not self.is_owner(post):
                    error = 'Edit other people posts is not allowed.'
                    self.render_post_form(error=error,
                                          subject=subject,
                                          content=content)
                else:
                    post.update(subject=subject, content=content)
                    post_url = "/blog/%s" % post_id
                    self.redirect(post_url, permanent=True)

class PostHandler(WelcomeHandler):
    """ Render the post detail and delete it """

    def get_page_stack(self):
        """
            Stack of current page label and url.
            Used to create a navigation component.
        """
        pages = super(PostHandler, self).get_page_stack()
        pages.append(Page(label='Post detail', url='/blog/%s' % self.post_id))
        return pages

    def get(self, post_id):
        """ handle /GET /blog/<blog_id> operation """
        if self.is_user_authenticated():
            self.post_id = post_id
            post = Post.by_id(int(post_id))
            comments = []

            for comment in post.comments:
                comments.append(Comment.by_id(comment.id()))

            if not post:
                self.redirect("/blog", permanent=True)
            else:
                self.render('blog_detail.html',
                            page=self,
                            post=post,
                            comments=comments)

    def delete(self, post_id):
        """ handle /DELETE /blog/<blog_id> operation """
        if self.is_user_authenticated():
            post = Post.by_id(int(post_id))

            if not post:
                self.write(json.dumps({"message": "Post already removed!"}))
            elif not self.is_owner(post):
                self.response.set_status(401)
                self.write("Remove other people posts is not allowed.")
            else:
                post.delete()
                self.write(json.dumps({"message": "Post removed!"}))

class LikeHandler(WelcomeHandler):
    """ Like/Unline a post. """

    def post(self, post_id):
        """ handle /POST /blog/<blog_id>/like operation """
        if self.is_user_authenticated():
            post = Post.by_id(int(post_id))

            if not post:
                self.response.set_status(401)
                self.write("Post not found.")
            elif self.is_owner(post):
                self.response.set_status(401)
                self.write("You can't like your own post.")
            else:
                post.toogle_like(self.user)
                self.write(json.dumps({"message": post.likes_number()}))


class CommentHandler(WelcomeHandler):

    def is_comment_owner(self, comment):
        """
            return True if the user is the
            owner of the comment, otherwise
            returns false
         """
        return comment.author.key().id() == self.user.key().id()

    def post(self, post_id):
        if self.is_user_authenticated():
            content = self.request.POST['content']
            post = Post.by_id(int(post_id))

            if not post:
                self.response.set_status(401)
                self.write("Post not found.")
            elif not content:
                self.response.set_status(401)
                self.write("Empty comment is not allowed.")
            else:
                post.add_comment(content=content, author=self.user)
                self.write(json.dumps({"message": "Comment added!"}))

    def put(self, comment_id):
        if self.is_user_authenticated():
            content = self.request.POST['content']
            comment = Comment.by_id(int(comment_id))

            if not comment:
                self.response.set_status(401)
                self.write("Comment not found.")
            elif not self.is_comment_owner(comment):
                self.response.set_status(401)
                self.write("You can't change other peoples comments.")
            else:
                comment.update_comment(content=content)
                self.write(json.dumps({"message": "Comment updated!"}))
