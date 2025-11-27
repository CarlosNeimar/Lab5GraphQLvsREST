const { ApolloServer } = require('@apollo/server');
const { startStandaloneServer } = require('@apollo/server/standalone');
const fs = require('fs');
const path = require('path');
const caminhoArquivo = path.join(__dirname, 'database.json');
const rawData = fs.readFileSync(caminhoArquivo, 'utf-8');
const COMMENTS_DATA = JSON.parse(rawData);

console.log(`[JS] Base de dados carregada com ${COMMENTS_DATA.length} registros.`);
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