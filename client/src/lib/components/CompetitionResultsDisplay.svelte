<script lang="ts">
    import { eventNames, type CompetitionResults } from '$lib/types';

    export let competitionResults: CompetitionResults;
</script>

<h1>Results for {competitionResults.competition.name}</h1>
<ul>
    {#each Object.entries(competitionResults.results) as [eventId, results]}
        <li>
            {eventNames[eventId as keyof typeof eventNames]}
        </li>
    {/each}
</ul>