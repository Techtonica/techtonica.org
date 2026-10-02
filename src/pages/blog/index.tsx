import React from 'react';
import Link from 'next/link';
import { blogPosts } from '../../data/blogPosts';

const BlogPage = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">Blog</h1>
      <div className="grid gap-8">
        {blogPosts.map((post) => (
          <article key={post.slug} className="border-b pb-8">
            <h2 className="text-2xl font-semibold mb-2">
              <Link href={`/blog/${post.slug}`} className="hover:text-blue-600 transition-colors">
                {post.title}
              </Link>
            </h2>
            <p className="text-gray-500 text-sm mb-3">{post.date}</p>
            <p className="text-gray-700 mb-4">{post.excerpt}</p>
            <Link href={`/blog/${post.slug}`} className="text-blue-500 font-medium hover:underline">
              Read more →
            </Link>
          </article>
        ))}
      </div>
    </div>
  );
};

export default BlogPage;
