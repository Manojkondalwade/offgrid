// OffGrid Platform - Mock Data Store
const OffGridData = {
  currentUser: {
    id: "u1",
    name: "Arjun Sharma",
    email: "arjun@college.edu",
    role: "student",
    avatar: "AS",
    branch: "CSE",
    year: 3,
    interests: ["tech", "hackathon", "ai", "music"],
    registeredEvents: [],
    votedPolls: []
  },

  events: [],
  polls: [],

  sponsors: [
    {
      id: "s1",
      name: "TechCorp India",
      logo: "🏢",
      industry: "Technology",
      budget: "₹10,000 - ₹50,000",
      interests: ["hackathon", "tech", "coding"],
      description: "Leading software company looking to connect with talented students.",
      proposals: []
    },
    {
      id: "s2",
      name: "DevHub",
      logo: "⚙️",
      industry: "Developer Tools",
      budget: "₹5,000 - ₹20,000",
      interests: ["workshop", "ai", "tech"],
      description: "Platform for developers. Supporting student communities building the future.",
      proposals: []
    },
    {
      id: "s3",
      name: "Startup India",
      logo: "🚀",
      industry: "Government Initiative",
      budget: "₹20,000 - ₹1,00,000",
      interests: ["startup", "seminar", "business"],
      description: "Government scheme supporting entrepreneurship and startup culture in colleges.",
      proposals: []
    },
    {
      id: "s4",
      name: "CloudNine Tech",
      logo: "☁️",
      industry: "Cloud Computing",
      budget: "₹15,000 - ₹60,000",
      interests: ["tech", "hackathon", "ai"],
      description: "Cloud infrastructure provider looking to sponsor innovative tech events.",
      proposals: []
    }
  ],

  proposals: [],
  notifications: [],

  clubs: [
    { id: "c1", name: "CodeDecode Club", emoji: "💻", category: "Technical", members: 120, events: 0 },
    { id: "c2", name: "Cultural Association", emoji: "🎭", category: "Cultural", members: 200, events: 0 },
    { id: "c3", name: "E-Cell", emoji: "🚀", category: "Entrepreneurship", members: 85, events: 0 },
    { id: "c4", name: "Robotics Club", emoji: "🦾", category: "Technical", members: 60, events: 0 }
  ]
};

OffGridData.getRecommended = function () {
  return [];
};

OffGridData.getEvent = function () {
  return null;
};

OffGridData.getPollForEvent = function () {
  return null;
};

window.OffGridData = OffGridData;
