import requests
import argparse
import yaml


def download_manifest(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download {url}")
        response.raise_for_status()


def append_annotations_to_crds(filename):
    with open(filename, 'r') as f:
        crds = list(yaml.safe_load_all(f))
        for crd in crds:
            if crd and crd.get('kind') == 'CustomResourceDefinition':
                crd.setdefault('metadata', {}).setdefault('annotations', {}).update({
                    'argocd.argoproj.io/sync-wave': '-1',
                    # 'argocd.argoproj.io/hook': 'PreSync'
                })

    with open(filename, 'w') as f:
        yaml.dump_all(crds, f)


def split_and_append_annotations_to_olm_manifests(filename):
    with open(filename, 'r') as f:
        resources = list(yaml.safe_load_all(f))
        olm_resources = []
        operators_resources = []
        namespace_resources = []

        for resource in resources:
            if resource is None:
                continue
            if resource.get('kind') == 'Namespace':
                namespace_resources.append(resource)
            elif resource.get('metadata', {}).get('namespace') == 'operators':
                operators_resources.append(resource)
            else:
                olm_resources.append(resource)

    # write_manifest('namespaces.yaml', namespace_resources, '0', 'Sync')
    write_manifest('olm.yaml', olm_resources, '1', 'Sync')
    write_manifest('operator-group.yaml', operators_resources, '1', 'Sync')


def write_manifest(filename, resources, sync_wave=None, hook=None):
    with open(filename, 'w') as f:
        for resource in resources:
            if sync_wave and hook and 'metadata' in resource:
                resource['metadata'].setdefault('annotations', {}).update({
                    'argocd.argoproj.io/sync-wave': sync_wave,
                    # 'argocd.argoproj.io/hook': hook
                })
            yaml.dump(resource, f)
            f.write('---\n')


def main(release):
    base_url = 'https://github.com/operator-framework/operator-lifecycle-manager/releases/download'
    if release:
        crds_url = f'{base_url}/{release}/crds.yaml'
        olm_url = f'{base_url}/{release}/olm.yaml'
    else:
        response = requests.get(
            'https://api.github.com/repos/operator-framework/operator-lifecycle-manager/releases/latest')
        latest_release = response.json().get('tag_name')
        crds_url = f'{base_url}/{latest_release}/crds.yaml'
        olm_url = f'{base_url}/{latest_release}/olm.yaml'

    download_manifest(crds_url, 'crds.yaml')
    download_manifest(olm_url, 'olm.yaml')

    append_annotations_to_crds('crds.yaml')
    split_and_append_annotations_to_olm_manifests('olm.yaml')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("release", nargs='?', help="Release version of OLM (optional)")
    args = parser.parse_args()
    main(args.release)
