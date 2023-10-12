## Workflow

- To review changes locally, run `quarto preview` (which calls `hugo serve` and automatically rerenders all changed `.qmd` and `.ipynb` files).

- To publish a new post online, run `quarto render` to render all `.qmd` and `.ipynb` files, then run `hugo` to build the site for publishing, and finally push all changes to GitHub.

- To update a post, first delete the relevant folder in the `public` directory (because this isn't updated automatically), then follow the same process as for publishing a new post. Do not delete the entire `public` folder (see below)!

- If the new post or updated post contains images, I have to move the folder `post-folder_files`, which, on rendering gets automatically created as a subfolder in `contents/posts/post-folder`, to `public/post-folder` because this unfortunately doesn't happen automatically. This is also the reason why I can't just delete teh entire `public` directory when any post.

## todo
- [x] Document workflow
- [x] Nice and clean homepage
- [x] Home button
- [x] Change url to homepage
- [x] Set up categories and tags
- [x] Move content from old blog
- [ ] Allow comments (useful resource [here](https://cloudcannon.com/jamstack-ecosystem/commenting/))
- [ ] Remove author field from posts (see [here](https://github.com/halogenica/beautifulhugo/issues/340))
- [ ] Turn photo into digital portrait
- [ ] Set up command to create new blog post with data in name and header
- [ ] Add book reviews in the form of Gerhard Pfister (short summaries)
- [ ] Add photos?

## Ideas for posts
- [ ] Revenue per employee for Basecamp and other companies (is basecamp really that efficient? What other companies are, too? Look into Twitter pre and post layoffs, look at Meta.)

## Useful resources
- [Hugo](https://gohugo.io/getting-started/quick-start/)
- [Quarto](https://quarto.org/docs/output-formats/hugo.html)
- [LoveIt](https://hugoloveit.com/theme-documentation-basics/)
- [LoveIt full docs](https://hugoloveit.com/theme-documentation-content/)
