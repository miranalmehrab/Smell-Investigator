with open("example.yaml", 'r') as stream:

    try:
        yaml.load(stream)
        print(yaml.load(stream))
    
    except yaml.YAMLError as exc:
        print(exc)
