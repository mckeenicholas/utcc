<script lang="ts">
	import { DatePicker } from 'bits-ui';
	import { type DateValue } from '@internationalized/date';

	let { selectedDate = $bindable() }: { selectedDate: DateValue | undefined } = $props();
</script>

<DatePicker.Root bind:value={selectedDate} weekdayFormat="short" fixedWeeks={true}>
	<div class="flex w-full flex-col gap-1.5">
		<DatePicker.Label class="block text-sm font-medium text-gray-700">
			Competition Date
		</DatePicker.Label>
		<DatePicker.Input
			class="flex w-full items-center rounded-md border border-gray-300 px-3 py-1 text-sm shadow-sm focus-within:border-gray-500 focus-within:ring-1 focus-within:ring-gray-500 hover:border-gray-400"
		>
			{#snippet children({ segments })}
				{#each segments as { part, value }, i (part + i)}
					<div class="-m-0.5 inline-block select-none">
						{#if part === 'literal'}
							<DatePicker.Segment {part} class="px-1 text-gray-500">
								{value}
							</DatePicker.Segment>
						{:else}
							<DatePicker.Segment
								{part}
								class="rounded px-1 py-1 hover:bg-gray-100 focus:bg-gray-100 focus:text-gray-900 focus-visible:ring-0 focus-visible:ring-offset-0 aria-[valuetext=Empty]:text-gray-400"
							>
								{value}
							</DatePicker.Segment>
						{/if}
					</div>
				{/each}
				<DatePicker.Trigger
					class="ml-auto inline-flex h-8 w-8 items-center justify-center rounded text-gray-600 transition-colors hover:bg-gray-100 hover:text-gray-800"
				>
					<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
						/>
					</svg>
				</DatePicker.Trigger>
			{/snippet}
		</DatePicker.Input>
		<DatePicker.Content sideOffset={6} class="z-50">
			<DatePicker.Calendar class="rounded-lg border border-gray-200 bg-white p-4 shadow-lg">
				{#snippet children({ months, weekdays })}
					<DatePicker.Header class="mb-4 flex items-center justify-between">
						<DatePicker.PrevButton
							class="inline-flex h-9 w-9 items-center justify-center rounded-md transition-colors hover:bg-gray-100"
						>
							<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M15 19l-7-7 7-7"
								/>
							</svg>
						</DatePicker.PrevButton>
						<DatePicker.Heading class="text-sm font-medium" />
						<DatePicker.NextButton
							class="inline-flex h-9 w-9 items-center justify-center rounded-md transition-colors hover:bg-gray-100"
						>
							<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M9 5l7 7-7 7"
								/>
							</svg>
						</DatePicker.NextButton>
					</DatePicker.Header>
					<div class="flex flex-col space-y-4">
						{#each months as month (month.value)}
							<DatePicker.Grid class="w-full border-collapse space-y-1">
								<DatePicker.GridHead>
									<DatePicker.GridRow class="mb-1 flex w-full justify-between">
										{#each weekdays as day (day)}
											<DatePicker.HeadCell class="w-9 rounded-md text-xs font-normal text-gray-500">
												<div>{day.slice(0, 2)}</div>
											</DatePicker.HeadCell>
										{/each}
									</DatePicker.GridRow>
								</DatePicker.GridHead>
								<DatePicker.GridBody>
									{#each month.weeks as weekDates (weekDates)}
										<DatePicker.GridRow class="flex w-full">
											{#each weekDates as date (date)}
												<DatePicker.Cell
													{date}
													month={month.value}
													class="relative h-9 w-9 p-0 text-center text-sm"
												>
													<DatePicker.Day
														class="data-selected:bg-gray-900 data-selected:text-white data-disabled:text-gray-300 data-disabled:pointer-events-none data-outside-month:pointer-events-none data-outside-month:text-gray-400 data-unavailable:text-gray-300 data-unavailable:line-through inline-flex h-9 w-9 items-center justify-center whitespace-nowrap rounded-md text-sm font-normal text-gray-900 transition-colors hover:bg-gray-100"
													>
														{date.day}
													</DatePicker.Day>
												</DatePicker.Cell>
											{/each}
										</DatePicker.GridRow>
									{/each}
								</DatePicker.GridBody>
							</DatePicker.Grid>
						{/each}
					</div>
				{/snippet}
			</DatePicker.Calendar>
		</DatePicker.Content>
	</div>
</DatePicker.Root>
