<script lang="ts">
import { slide } from "svelte/transition";
import { Collapsible } from "bits-ui";
import { eventNames, type ScrambleKey, type WCAEvent } from "$lib/types";
import { scrambleOrder } from "$lib/utils";
import CubeIcon from "./CubeIcon.svelte";

interface ScrambleItem {
	num: string;
	scramble: string;
}

interface ScrambleSetItem {
	num: number;
	scrambles: ScrambleItem[];
}

interface ScrambleRoundItem {
	roundNum: number;
	sets: ScrambleSetItem[];
}

interface EventScrambleData {
	event: WCAEvent;
	rounds: ScrambleRoundItem[];
}

const { eventScramble }: { eventScramble: EventScrambleData } = $props();

let open = $state(false);
</script>

<div class="overflow-hidden border border-gray-200 bg-white">
	<Collapsible.Root bind:open>
		<Collapsible.Trigger class="w-full bg-white transition-colors duration-100 ease-in-out hover:bg-gray-50">
			<div class="flex items-center justify-between px-4 py-2.5">
				<div class="flex items-center space-x-3">
					<CubeIcon event={eventScramble.event} />
					<h3 class="text-base font-bold text-gray-900">
						{eventNames[eventScramble.event]}
					</h3>
				</div>
				<svg
					class="h-5 w-5 text-gray-700 transition-transform duration-200 ease-in-out"
					class:rotate-180={open}
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24"
				>
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
				</svg>
			</div>
		</Collapsible.Trigger>

		<Collapsible.Content class="border-t border-gray-200" forceMount>
			{#if open}
				<div class="space-y-6 px-6 py-4" transition:slide>
					{#each eventScramble.rounds as scrambleRound (scrambleRound.roundNum)}
						<div>
							<p class="text-sm font-semibold text-gray-900">
								Round {scrambleRound.roundNum}
							</p>

							<div class="mt-3 space-y-4">
								{#each scrambleRound.sets as scrambleSet (scrambleSet.num)}
									<div>
										<h5
											class="border-b border-gray-200 pb-2 text-xs font-semibold tracking-wider text-gray-700 uppercase"
										>
											Scramble Set {scrambleSet.num}
										</h5>

										{#each scrambleSet.scrambles as scramble (scramble.num)}
											<div class="border-b border-gray-100 p-3 last:border-b-0">
												<div class="flex flex-col gap-2 sm:flex-row sm:items-start">
													<span
														class="me-8 w-4 min-w-fit text-center align-middle text-xs font-medium tracking-wider text-gray-700 uppercase"
													>
														{scrambleOrder[scramble.num as ScrambleKey]?.name ?? scramble.num}
													</span>
													<code class="font-mono text-xs break-all whitespace-pre-wrap text-gray-800">
														{scramble.scramble}
													</code>
												</div>
											</div>
										{/each}
									</div>
								{/each}
							</div>
						</div>
					{/each}
				</div>
			{/if}
		</Collapsible.Content>
	</Collapsible.Root>
</div>
