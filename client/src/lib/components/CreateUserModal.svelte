<script lang="ts">
import { Portal } from "bits-ui";
import { type User, studentDesignatorOptions } from "$lib/types";
import { createUser } from "$lib/userService";
import SelectMenu from "./SelectMenu.svelte";

let {
	show,
	initialName = $bindable(""),
	onClose,
	onUserCreated,
}: {
	show: boolean;
	initialName?: string;
	onClose: () => void;
	onUserCreated: (user: User) => void;
} = $props();

let creatingUser = $state(false);
let studentDesignator = $state("UTSG");

const handleCreateUser = async () => {
	if (!initialName.trim()) {
		return;
	}
	creatingUser = true;

	try {
		const response = await createUser(initialName, studentDesignator);
		if (response.ok) {
			const newUser: User = await response.json();
			onUserCreated(newUser);
			onClose();
		}
	} catch (error) {
		console.error("Failed to create user:", error);
	} finally {
		creatingUser = false;
	}
};

$effect(() => {
	if (show) {
		const originalOverflow = document.body.style.overflow;
		document.body.style.overflow = "hidden";
		return () => {
			document.body.style.overflow = originalOverflow;
		};
	}
});
</script>

{#if show}
	<Portal>
		<div
			class="fixed inset-0 z-50 flex h-full min-h-dvh w-full items-center justify-center bg-black/50 p-4 backdrop-blur-xs"
			onclick={onClose}
			onkeydown={(e) => e.key === "Escape" && onClose()}
			aria-label="Close modal"
			role="button"
			tabindex="0"
		>
			<div
				class="w-full max-w-md border border-border-strong bg-surface p-6"
				role="dialog"
				aria-modal="true"
				tabindex="0"
				onclick={(e) => e.stopPropagation()}
				onkeydown={(e) => e.key === "Escape" && onClose()}
			>
				<h3 class="mb-4 text-base font-bold text-main">Add New Competitor</h3>
				<div class="space-y-4">
					<div>
						<label for="user-name" class="block text-xs font-semibold tracking-wider text-secondary uppercase"
							>Person Name</label
						>
						<input
							type="text"
							id="user-name"
							bind:value={initialName}
							placeholder="Enter competitor name"
							class="mt-1 w-full rounded-sm border border-border-strong bg-surface px-3 py-1.5 text-sm text-main placeholder:text-muted focus:border-brand focus:ring-1 focus:ring-brand focus:outline-none"
						/>
					</div>
					<div>
						<label for="student-status" class="block text-xs font-semibold tracking-wider text-secondary uppercase">
							Designation
						</label>
						<div class="mt-1">
							<SelectMenu bind:value={studentDesignator} options={studentDesignatorOptions} />
						</div>
					</div>
				</div>

				<div class="mt-6 flex justify-end space-x-2 border-t border-border pt-4">
					<button
						type="button"
						onclick={onClose}
						class="rounded-sm border border-border bg-surface px-3 py-1.5 text-xs font-medium text-secondary transition-colors hover:bg-surface-muted"
					>
						Cancel
					</button>
					<button
						type="button"
						onclick={handleCreateUser}
						disabled={creatingUser || !initialName.trim()}
						class="rounded-sm bg-uoft-blue px-3 py-1.5 text-xs font-medium text-white transition-colors hover:bg-uoft-blue-80 disabled:opacity-50 dark:border dark:border-blue-500/30 dark:hover:bg-blue-900"
					>
						{creatingUser ? "Creating..." : "Create Competitor"}
					</button>
				</div>
			</div>
		</div>
	</Portal>
{/if}
