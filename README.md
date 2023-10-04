## Workflow

- To review changes locally, run `quarto preview` (which calls `hugo serve` and automatically rerenders all changed `.qmd` and `.ipynb` files).

- To push changes online, delete the `public` directory, run `quarto render` to render all `.qmd` and `.ipynb` files, then run `hugo`, to build the site for publishing. After that, just push all changes to GitHub.

- Images are not automatically rendered, because the folder that contains images `post-folder-name_files` -- which, on rendering gets automatically created as a subfolder in `post-folder-name` in `contents/posts` -- isn't automatically moved to `public/post-folder-name`. So I have to move it manually for post images to be rendered.


## todo
- [x] Document workflow
- [x] Nice and clean homepage
- [x] Home button
- [x] Change url to homepage
- [x] Set up categories and tags
- [ ] Allow comments (useful resource [here](https://cloudcannon.com/jamstack-ecosystem/commenting/))
- [ ] Remove author field from posts (see [here](https://github.com/halogenica/beautifulhugo/issues/340))
- [ ] Turn photo into digital portrait
- [ ] Move content from old blog
- [ ] Set up command to create new blog post with data in name and header
- [ ] Add book reviews in the form of Gerhard Pfister (short summaries)
- [ ] Add photos

## Ideas for posts
- [ ] Revenue per employee for Basecamp and other companies (is basecamp really that efficient? What other companies are, too? Look into Twitter pre and post layoffs, look at Meta.)

## Useful resources
- [Hugo](https://gohugo.io/getting-started/quick-start/)
- [Quarto](https://quarto.org/docs/output-formats/hugo.html)
- [LoveIt](https://hugoloveit.com/theme-documentation-basics/)
- [LoveIt full docs](https://hugoloveit.com/theme-documentation-content/)
