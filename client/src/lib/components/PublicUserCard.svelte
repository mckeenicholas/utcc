<script lang="ts">
import type { User } from "$lib/types";

interface Props {
	user: User;
}

const { user }: Props = $props();
</script>

<a href="/persons/{user.id}" class="group block">
	<div
		class="flex w-full cursor-pointer items-center justify-between border border-gray-200 bg-white p-3 transition-colors hover:border-uoft-blue"
	>
		<div class="flex min-w-0 items-center gap-3">
			<div
				class="flex h-8 w-8 shrink-0 items-center justify-center rounded-sm bg-gray-100 text-xs font-bold text-uoft-blue transition-colors group-hover:bg-uoft-blue group-hover:text-white"
			>
				{user.name.charAt(0).toUpperCase()}
			</div>
			<div class="truncate">
				<p class="truncate text-sm font-medium text-gray-900 transition-colors group-hover:text-uoft-blue">
					{user.name}
				</p>
				{#if user.student_designator}
					<span class="rounded-sm bg-gray-100 px-1.5 py-0.5 text-[10px] font-medium text-gray-600 uppercase">
						{user.student_designator}
					</span>
				{/if}
			</div>
		</div>

		<span class="text-xs text-gray-400 transition-colors group-hover:text-uoft-blue">&rarr;</span>
	</div>
</a>
