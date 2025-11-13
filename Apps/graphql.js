const { ApolloServer } = require('@apollo/server');
const { startStandaloneServer } = require('@apollo/server/standalone');

const COMMENTS_DATA = [
    { id: "1", userId: "13", score: 3, text: "This is okay." },
    { id: "2", userId: "10", score: 8, text: "Amazing!" },
    { id: "3", userId: "13", score: 9, text: "My favorite one." },
    { id: "4", userId: "11", score: 5, text: "Not bad." },
    { id: "5", userId: "10", score: 1, text: "Terrible." },
];

const typeDefs = `#graphql
  type Comment {
    id: ID!
    userId: ID!
    score: Int
    text: String
  }

  type Query {
    allComments: [Comment]
    commentById(id: ID!): Comment
    commentsByUserId(id: ID!): [Comment]
    commentsByMinScore(score: Int!): [Comment]
  }
`;

const resolvers = {
    Query: {
        allComments: () => COMMENTS_DATA,
        commentById: (parent, args) => {
            return COMMENTS_DATA.find(c => c.id === args.id);
        },
        commentsByUserId: (parent, args) => {
            return COMMENTS_DATA.filter(c => c.userId === args.id);
        },
        commentsByMinScore: (parent, args) => {
            return COMMENTS_DATA.filter(c => c.score >= args.score);
        },
    },
};

const server = new ApolloServer({ typeDefs, resolvers });

startStandaloneServer(server, { listen: { port: 3001 } })
    .then(({ url }) => {
        console.log(`[JS] Servidor GraphQL rodando em ${url}`);
    });