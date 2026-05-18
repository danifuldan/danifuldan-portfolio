import markdownIt from "markdown-it";
import markdownItAnchor from "markdown-it-anchor";

export default function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy("src/css");
  eleventyConfig.addPassthroughCopy("src/img");

  const md = markdownIt({ html: true, linkify: true, typographer: true })
    .use(markdownItAnchor, {
      permalink: markdownItAnchor.permalink.headerLink({ safariReaderFix: true }),
      level: [2, 3],
    });

  eleventyConfig.setLibrary("md", md);

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
  };
}
