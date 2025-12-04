const { ApolloServer, gql } = require('apollo-server');
const fs = require('fs');

const rawData = fs.readFileSync('../Data/database_100k_user.json');
const db = JSON.parse(rawData);

const typeDefs = gql`
  type Post {
    id: ID!
    title: String
    content: String
    published: Boolean
  }

  type User {
    id: ID!
    name: String
    email: String
    address: String
    company: String
    posts: [Post]
  }

  type Query {
    # Adicionado argumento limit
    users(limit: Int): [User] 
    user(id: ID!): User
  }
`;

const resolvers = {
    Query: {
        users: (_, { limit }) => limit ? db.users.slice(0, limit) : db.users,
        user: (_, { id }) => db.users.find(u => u.id == id),
    },
    User: {
        posts: (parent) => db.posts.filter(p => p.user_id == parent.id),
    },
};

const server = new ApolloServer({ typeDefs, resolvers });

server.listen({ port: 4001 }).then(({ url }) => {
    console.log(`Node GraphQL rodando em ${url}`);
});