######
## CENTRALITY
#####

# eigen centrality score for each node
eigen_centrality(X)$vector

# closeness centrality score for each node
closeness(net_3)

# betweenness centrality score for each node
betweenness(net_3)


######
## CLIQUES AND CLUSTERING
#####

# how many members does the largest clique have
clique_num(X)

# nodes who are members of the largest clique
largest.cliques(X)[[1]]

# avg clustering
transitivity(X, type = "average")

# how many & which nodes to erase, in order to split network into 2 unconnected groups
min_cut(X, value.only = FALSE)


######
## DISTANCE MEASURES
#####

# distribution of node's number of connections 
rethinking::dens(degree(X))

# summary table of various distance measures
tibble(
  "measure" = c("mean distance", "diameter", "mean degree"),
  "value" = c(mean(distances(net_3)), diameter(net_3), mean(degree(net_3)))
) %>%
  knitr::kable(digits = 2)