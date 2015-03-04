
# General Intro

Work is integrative (museum to theory)?

I am generally interested in understanding the processes underlying
biological diversification

I develop computational methods for inferring the evolutionary
relationships ... in time and space? for genomic data

fieldwork, NGS sequencing, apply methods, test for evolutionary patterns
predicted by processes of interest.


# Inferring evolutionary history

## Intro

A lot of my recent work has focused on how community-scale processes
affect diversification

Current phylogenetic methods assume that speciation/branching events and
extinction across the tree occur independently of one another through time.


### Violations

There are a lot of reasons we expect this assumption to be violated:

*   Vicariance
    +   break up of continents
    +   orogeny

*   Parasite communities co-evolving with their hosts

*


All of these examples have one thing in common:

They are processes that affect whole communities of co-distributed populations
of organisms

Given the dynamic nature of this planet, such community-scale processes are
likely very common

### Why care?

Why account for these violations?

1.  If we explicitly model the processes underlying the violations
    we may improve inference of the tree and divergence times

2.  Provide a general framework for inferring the affect of community-scale
    events on diversification

    *   This could have implications from plate tectonics to epidemiology!


**How can we do model large-scale processes?**

# Empirical example

To formulate my initial approach to this problem, let's use a
specific example

## SE Asia

A great example is SE Asian (birthplace of biogeography), which looked
something like this 20,000 years ago, whereas this is what we see today.

It seems intuitive that such wholesale island fragmentation could cause
speciation across whole communities of populations.

What sort of patterns does this predict?

Well, let's say that we went to the Philippine islands, and we went to two islands
that were previously connected during glacial periods and sampled three
species of lizards that are co-distributed across the two islands

If a rise in sea levels that fragmented the islands caused these populations to
diverge, we might expect their divergence times to be clustered and correspond
with the onset of an interglacial period.

Well, I decided to take a model-choice approach to this problem, and thought of
this as a particular divergence model, one in which there is a single
divergence-time parameter.

However, to take a model-choice approach to this problem, we have to consider
other possible models of divergence.

For example, we can add a second divergence-time parameter to the model,
and if we do so, we can assign our first, second, or third species to the new
divergence-time parameter.  These are three additional models of
divergence, in which two of the three pairs co-diverge.

There's also a fifth possible model, where there is no co-divergence, and all
three species diverge at unique times.

Ok, for the simple example of 3 pairs of populations, there are five possible
models of divergence, 4 of which include co-divergence.

What we want to be able to do is jointly estimate the model of divergence AND
the divergence times of the taxa.

How can we do this?

Well, we can collect sequence data from these populations.  These sequences
contain information about the genealogy across which they evolved,
which in turn has information about the size and time of divergence of the
populations.

So we need to model 
1.  the genealogy,
2.  the processes of nucleotide substitutions by which the sequences evolved
    along the geneology, and
3.  the demographic processes of the populations which control the branching
    rate of the gene trees.

These are all nuisance parameters; we are not interested in estimating
them, but they are necessary to link our data to the parameters of interest;
and we want to account for uncertainty.

For simplicity we will lump them all into theta.

This is a very parameter rich and stochastic model, so there is a lot
of expected variation. In order to accommodate (or more specifically integrate over)
that uncertainty, I decided to take a Bayesian model choice approach

to

estimate the divergence times of the taxa given the sequence data and a given
model of divergence using bayes rule, where we weight the likelihood by the
prior, and divide by the marginal probability of the data under this model.

If we sample over all the models of divergence, we can also leverage
bayes rule again to estimate the posterior probability of a given
model of divergence, which is the marginal likelihood of the model
weighted by the prior of the model.

We are actually going to do this jointly, but I like to separate out the
parameter estimation from the model-choice, because it drives home a very
important point.

We can see that in Bayesian model choice, we are essentially choosing the 
model with the best marginal likelihood.

What is the marginal likelihood?

Well, it might look a little scary, but its just an average likelihood.
We are simply taking the average of the likelihood over the entire parameter
space of the model, and we are weighting that average by the prior
probability of the parameters.

    In parameter estimation, this average over the priors is only a normalizing
    constant.
    
    Where in model-choice, the average likelihood over the priors is how
    the data inform the posterior probability.
    
    As a result, Bayesian model-choice tends to be much more sensitive to the prior
    assumptions about the parameters than parameter estimation.


???
We can't solve all of these integrals analytically, so we are going
to have to use numerical approximation.

Furthermore, I decided to that an approximate-likelihood approach
to the problem, which uses simulations to circumvent ever having
to derive or calculate the likelihood function.

Show ABC animation???
???


## Sampling models is hard

Sampling over these models, and more specifically specifying a prior to
all of them is not trivial

The number of models increases VERY rapidly.

## DPP

The model choice problem boils down to estimating the number of divergence
events and the assignment of the taxa to these divergence event.


???
?Previous methods assigned prior to the number of events??? show problem with that here.?
???


I developed a Dirichlet process prior to model the divergence models.

DPP is popular in Bayesian nonparametric statistics in situations such as this
where we are assigning variables to an unknown number of categories

The Dirichlet process is scary complicated (infinite mixture of Dirichlet
distributions...), but the basic concept is very simple.

The process works by adding one element at a time following a very
simple rule and a single parameter.

We start by assigning our first species to a divergence-time parameter
with probability of 1.0, because it has to go somewhere!

Next, we either assign the second species to the same divergence-time parameter
as the first species (with prob 1/alpha+1), or assign it to a new
divergence-time parameter (with prob alpha/alpha+1).

Then third species...

This provides a mathematically convenient way of assigning prior probabilities to
all possible models of divergence,

and its flexible!

We can decrease the concentration parameter to favor models with more
divergences (less shared divergence)

Or increase it to favor clustered models with fewer divergence events



## NEW METHOD

Developed new method
1.  flexible priors on parameters to avoid strongly weighting model posterior
    probablities
2.  a Dirichlet-process prior (DPP) over all possible divergence models
3.  Multi-processing to accommodate genomic datasets

## Simulations to assess performance

## Empirical application

Part of large collaboration to understand the affects of Pleistocene climate
cycles on diversification within the Philippines

For 22 taxa we sampled sequence data from two islands that were fragmented
during interglacials.

These taxa represent a broad diversity of vertebrates:
megachiropteran bats
microchiropteran bats
shrews
lizards
snakes
frogs

The results support 5-6 divergence events that were shared across these 22 taxa.

This is very interesting, because that is how many sea level fluctuations that
have been posited as important for these islands.

BUT! A lot of uncertainty here!

This uncertainty has motivated what I am currently working on...

## More data

We are currently working on collecting NGS data from these taxa from
across the Philippines

Pending pre-proposal to fund this

Very Prelim results

Further support for shared evolutionary history!

## More power

### Full likelihood

Currently working on implementing this approach in a full likelihood framework

Working with a great group of collaborators, and plan to implement in revbayes

# Next step

Full phylogenetic framework

1.  If we explicitly model the processes underlying the violations
    we may improve inference of the tree and divergence times

2.  Provide a general framework for inferring the affect of community-scale
    events on diversification

    *   This could have implications from plate tectonics to epidemiology!

Joke to name method AUBBIE or WAREAGLE or AUBURN of TIGER

   Analytical
solUtions for
   Bayesian
   Biogeographic
   Inference of
co-Evolution

Temporal
Inference of
Group-wise
Evolutionary
Relationships

W
A
R
E
A
G
L
E

# Empirical work

A large motivation for this theoretical and computational work is applying
these novel methods to empirical systems to better understand diversification
in biodiverse regions of the planet





---------------------------------

# Adventure 2

One great example of this is SE Asia, which has had a very dynamic landscape
over the past few million years.

During interglacial periods, SE Asia looked similar to what we see today.

But, during glacial periods, when sea levels dropped, the landscape was much
more extensive, and there was much more connectivity among land masses.

This happened repeatedly, where landmasses coalesced during glacial periods and
were fragmented during interglacial rises in sea levels.

This has been proposed as a model of diversification in SE Asia.

How do we test the predictions of this model?

My idea was to take a Bayesian model choice approach to this question.

To explain this approach let's zoom in on the Philippines for an example.

Let's say we went out to two islands (negros and panay), and sampled
three species of lizards that are co-distributed across both islands.

If a community-scale event (like sea level rise) had an affect on these
populations, we might expect to find the divergences times of these
three pairs of lizard populations to be clustered and correspond with
an interglacial rise in sea level.

We can think of this as a particular model of divergence, one in which there is
a single divergence-time parameter shared by all three species of lizard.
In other words, all three pairs of populations co-diverged.

However, this is only one possible model of divergence, and if we want to 
take a model choice approach to this problem, we have to consider other
possible models of divergence.

For example, we can add a second divergence-time parameter to the the model,
and if we do so, we can assign our first, second, or third species to the new
divergence-time parameter.  So, these are three additional models of
divergence, in which two of the three pairs co-diverge

There's also a fifth possible model, where there is no co-divergence, and all
three species diverge at unique times.

*   Need transition here to pop divergences, seq data, nuisance parameters

So, we have 5 possible models of divergence in this example with three
pairs of populations,

**and what we want to be able to do is infer both the model of divergence across
the taxa, and the divergence times of the taxa.**

