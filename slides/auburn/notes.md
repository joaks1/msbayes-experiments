
# General Intro

My interests and what I do

A lot of my recent work has focused on how community-scale processes
affect diversification

Current phylogenetic methods assume that speciation/branching events and
extinction across the tree occur independently of one another through time.

There are a lot of reasons we expect this assumption to be violated,
including processes that affect whole communities of co-distributed
populations of organisms

Why account for these violations?

1.  If we explicitly model the processes underlying the violations
    we may improve inference of the tree and divergence times

2.  Provide a general framework for inferring the affect of community-scale
    events on diversification

3.  save this for later... Possible epidemiological applications

# Adventure 1

How can we do model large-scale processes?

I decided to approach this problem from the simplest case first to figure out
what sort of patterns these processes predict and how we might infer them

For example, let's say we have a community of co-distributed species, and at
some point in the past an event split this community.

If we go out today and look at three species of lizards that are co-distributed
across the barrier, we might expect that their divergences are clustered around
the time of the event.

We can think of this as a particular model of divergence, one in which there is
a single divergence-time parameter.

However, if we want to take a model-choice approach to this problem, we
have to consider other possible models of divergence.

For example, we can add a second divergence-time parameter to the the model,
and if we do so, we can assign our first, second, or third species to the new
divergence-time parameter.  So, these are three additional models of
divergence, in which two of the three pairs co-diverge

There's also a fifth possible model, where there is no co-divergence, and all
three species diverge at unique times.

Ok, for the simple example of 3 pairs of populations, there are five possible
models of divergence, 4 of which include co-divergence.

We want to be able to jointly estimate the model of divergence AND the
divergence times of the taxa.

How can we do this?

Well, we can collect sequence data from these populations.  These sequences
contain information about the geneology across which they evolved,
which in turn has information about the size and time of divergence of the
populations.

So we can model the genealogy and the processes of nucleotide substitutions by
which the sequences evolved along the geneology.
We can also model the demographic processes of the populations which control
the branching rate of the gene trees.

The gene trees, mutational and demographic parameters are all nuisance
parameters, which for simplicity we will lump into theta.

If we accomodate all of this, we can estimate the divergence times
of the taxa given the sequence data and a given model of divergence using
bayes rule, where we weight the likelihood by the prior, and
divide by the marginal probability of the data under this model.

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

We can't solve all of these integrals analytically, so we are going
to have to use numerical approximation.

Furthermore, I decided to that an approximate-likelihood approach
to the problem, which uses simulations to circumvent ever having
to derive or calculate the likelihood function.

The approach used
1.  flexible priors on parameters to avoid strongly weighting model posterior
    probablities
2.  a Dirichlet-process prior (DPP) over all possible divergence models
3.  Multi-processing to accommodate genomic datasets

## Highlight DPP model here?

## Simulations to assess performance

## Empirical application


## More data

Prelim results

## More power

Full likelihood

Full phylogenetic framework

Joke to name method AUBBIE or WAREAGLE or AUBURN of TIGER


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

