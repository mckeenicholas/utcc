<script lang="ts">
import type { ClassValue } from "svelte/elements";
import { Label, Switch, useId } from "bits-ui";

let {
	id = useId(),
	label,
	checked = $bindable(false),
	class: classProps,
}: { id?: string; label: string; checked?: boolean; class?: ClassValue } = $props();
</script>

<div class="me-2 flex items-center gap-x-2 {classProps}">
	<Switch.Root
		bind:checked
		{id}
		class="peer inline-flex h-5.5 min-h-5.5 w-11 shrink-0 cursor-pointer items-center rounded-full px-0.5 transition-colors focus-visible:ring-2 focus-visible:ring-brand focus-visible:ring-offset-1 focus-visible:outline-hidden disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-uoft-blue data-[state=unchecked]:bg-surface-muted dark:focus-visible:ring-blue-400 dark:data-[state=checked]:bg-blue-600"
	>
		<Switch.Thumb
			class="pointer-events-none block size-4.5 shrink-0 rounded-full bg-white transition-transform data-[state=checked]:translate-x-5.5 data-[state=unchecked]:translate-x-0"
		/>
	</Switch.Root>
	<Label.Root for={id} class="cursor-pointer text-xs font-medium text-secondary select-none">{label}</Label.Root>
</div>
