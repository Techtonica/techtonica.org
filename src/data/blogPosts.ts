export interface BlogPost {
  title: string;
  slug: string;
  date: string;
  excerpt: string;
  content: string;
  coverImage?: string;
}

export const blogPosts: BlogPost[] = [
  {
    title: "Welcome to Techtonica",
    slug: "welcome-to-techtonica",
    date: "2023-01-15",
    excerpt: "Learn how Techtonica is changing the way people enter the tech industry.",
    content: "Full content migrated from Medium regarding the mission and vision of Techtonica...",
  },
  {
    title: "The Future of Software Engineering",
    slug: "future-of-software-engineering",
    date: "2023-05-20",
    excerpt: "Exploring the impact of AI and autonomous agents on the coding landscape.",
    content: "Detailed analysis of the evolving role of the software engineer...",
  },
];
